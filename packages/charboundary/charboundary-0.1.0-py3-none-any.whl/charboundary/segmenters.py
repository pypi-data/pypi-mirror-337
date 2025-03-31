"""
Text segmentation functionality for the charboundary library.
"""

import gzip
import json
import os
import pickle
import tempfile
from dataclasses import dataclass, field
from typing import (
    List, 
    Tuple, 
    Dict, 
    Any, 
    Optional, 
    Union, 
    Protocol, 
    TypeAlias, 
    Iterator,
    Literal,
    TypedDict
)
import random

import sklearn.metrics
from skops.io import dump, load

from charboundary.constants import (
    SENTENCE_TAG, 
    PARAGRAPH_TAG, 
    TERMINAL_SENTENCE_CHAR_LIST, 
    TERMINAL_PARAGRAPH_CHAR_LIST,
    DEFAULT_ABBREVIATIONS
)
from charboundary.encoders import CharacterEncoder, CharacterEncoderProtocol
from charboundary.features import (
    FeatureExtractor, 
    FeatureExtractorProtocol, 
    FeatureVector,
    FeatureMatrix,
    PositionLabels
)
from charboundary.models import create_model, TextSegmentationModel


class MetricsResult(TypedDict):
    """Type definition for metrics result dictionary."""
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    boundary_accuracy: float
    binary_mode: bool


@dataclass
class SegmenterConfig:
    """Configuration parameters for TextSegmenter."""
    left_window: int = 5
    right_window: int = 5
    abbreviations: List[str] = field(default_factory=lambda: DEFAULT_ABBREVIATIONS.copy())
    model_type: str = "random_forest"
    model_params: Dict[str, Any] = field(default_factory=lambda: {
        "n_estimators": 100,
        "max_depth": 16,
        "min_samples_split": 2,
        "min_samples_leaf": 1,
        "n_jobs": -1,
        "class_weight": "balanced"
    })
    use_numpy: bool = True
    cache_size: int = 1024
    num_workers: int = 0  # Auto-detect


class TextSegmenterProtocol(Protocol):
    """Protocol defining the interface for text segmenters."""
    
    def train(self, data: Union[str, List[str]], **kwargs) -> MetricsResult:
        """Train a new model for text segmentation."""
        ...
    
    def segment_text(self, text: str) -> str:
        """Segment text into sentences and paragraphs."""
        ...
    
    def segment_to_sentences(self, text: str) -> List[str]:
        """Segment text into a list of sentences."""
        ...
    
    def segment_to_paragraphs(self, text: str) -> List[str]:
        """Segment text into a list of paragraphs."""
        ...
    
    def evaluate(self, data: Union[str, List[str]], **kwargs) -> MetricsResult:
        """Evaluate the model on a dataset."""
        ...


class TextSegmenter:
    """
    High-level interface for training, saving, loading, and using text segmentation models.
    
    This simplified implementation only supports binary classification (boundary/non-boundary).
    """

    def __init__(
            self,
            model: Optional[TextSegmentationModel] = None,
            encoder: Optional[CharacterEncoderProtocol] = None,
            feature_extractor: Optional[FeatureExtractorProtocol] = None,
            config: Optional[SegmenterConfig] = None,
    ):
        """
        Initialize the TextSegmenter.

        Args:
            model (TextSegmentationModel, optional): Model to use.
                If None, a model will be created when training.
            encoder (CharacterEncoderProtocol, optional): Character encoder to use.
                If None, a new one will be created.
            feature_extractor (FeatureExtractorProtocol, optional): Feature extractor to use.
                If None, a new one will be created.
            config (SegmenterConfig, optional): Configuration parameters.
                If None, default configuration will be used.
        """
        self.config = config or SegmenterConfig()
        
        self.encoder = encoder or CharacterEncoder()
        
        self.feature_extractor = feature_extractor or FeatureExtractor(
            encoder=self.encoder,
            abbreviations=self.config.abbreviations,
            use_numpy=self.config.use_numpy,
            cache_size=self.config.cache_size
        )
        
        self.model = model
        self.is_trained = model is not None

    def train(
            self,
            data: Union[str, List[str]],
            sample_rate: float = 0.1,
            max_samples: Optional[int] = None,
            model_type: Optional[str] = None,
            model_params: Optional[Dict[str, Any]] = None,
            left_window: Optional[int] = None,
            right_window: Optional[int] = None,
            num_workers: Optional[int] = None,
    ) -> MetricsResult:
        """
        Train a new model for text segmentation.

        Args:
            data (Union[str, List[str]]):
                - Path to a training data file
                - List of annotated texts
            sample_rate (float, optional): Rate at which to sample non-terminal positions.
                Defaults to 0.1.
            max_samples (int, optional): Maximum number of samples to process.
                If None, process all samples.
            model_type (str, optional): Type of model to use.
                If None, use the value from config.
            model_params (Dict[str, Any], optional): Parameters for the model.
                If None, use the values from config.
            left_window (int, optional): Size of left context window.
                If None, use the value from config.
            right_window (int, optional): Size of right context window.
                If None, use the value from config.
            num_workers (int, optional): Number of worker processes for parallel processing.
                If None, use the value from config.

        Returns:
            MetricsResult: Training metrics
        """
        # Update config with new values, if provided
        if left_window is not None:
            self.config.left_window = left_window
        if right_window is not None:
            self.config.right_window = right_window
        if num_workers is not None:
            self.config.num_workers = num_workers
        if model_type is not None:
            self.config.model_type = model_type
        if model_params is not None:
            self.config.model_params.update(model_params)

        features: FeatureMatrix = []
        labels: PositionLabels = []

        # Process data
        if isinstance(data, str):
            # Path to a file
            if data.endswith('.jsonl.gz'):
                # Handle gzipped jsonl files
                with gzip.open(data, 'rt', encoding='utf-8') as f:
                    i = 0
                    for line in f:
                        if max_samples is not None and i >= max_samples:
                            break
                        try:
                            json_obj = json.loads(line.strip())
                            if 'text' in json_obj:
                                self._process_text_for_training(json_obj['text'], features, labels, sample_rate)
                                i += 1
                        except json.JSONDecodeError:
                            print(f"Warning: Skipping invalid JSON line in {data}")
            else:
                # Handle regular text files
                with open(data, "r", encoding="utf-8") as input_file:
                    texts = input_file.readlines()
                    for i, text in enumerate(texts):
                        if max_samples is not None and i >= max_samples:
                            break
                        self._process_text_for_training(text, features, labels, sample_rate)
        elif isinstance(data, list):
            for i, text in enumerate(data):
                if max_samples is not None and i >= max_samples:
                    break
                self._process_text_for_training(text, features, labels, sample_rate)
        
        # Create and train the model
        self.model = create_model(
            model_type=self.config.model_type, 
            **(self.config.model_params)
        )
        
        # Print debug info about the training data
        print(f"Training on {len(features)} samples...")
        print(f"Window sizes: left={self.config.left_window}, right={self.config.right_window}")
        print(f"Positive samples (boundaries): {labels.count(1)}")
        print(f"Negative samples (non-boundaries): {labels.count(0)}")
        print(f"Positive ratio: {labels.count(1) / len(labels) if labels else 0:.4f}")
        
        # Fit the model
        self.model.fit(X=features, y=labels)
        self.is_trained = True

        # Evaluate on training data
        report = self.model.get_metrics(features, labels)

        return report

    def _process_text_for_training(
            self,
            text: str,
            features: FeatureMatrix,
            labels: PositionLabels,
            sample_rate: float = 0.1,
    ) -> None:
        """
        Process a text for training and add its features and labels to the provided lists.

        Args:
            text (str): Annotated text
            features (FeatureMatrix): List to which features will be added
            labels (PositionLabels]): List to which labels will be added
            sample_rate (float, optional): Rate at which to sample non-terminal positions.
                Defaults to 0.1.
        """
        clean_text, text_features, text_labels = self.feature_extractor.process_annotated_text(
            text, 
            self.config.left_window, 
            self.config.right_window,
            self.config.num_workers
        )

        # Always include terminal characters and a sample of non-terminal characters
        for j, (char, feature_vec, label) in enumerate(zip(clean_text, text_features, text_labels)):
            is_terminal = char in TERMINAL_SENTENCE_CHAR_LIST or char in TERMINAL_PARAGRAPH_CHAR_LIST
            
            # Use modern Python 3.11 pattern matching for cleaner code
            match (label, is_terminal, random.random() < sample_rate):
                case (1, _, _):  # Always include positive samples (boundaries)
                    features.append(feature_vec)
                    labels.append(label)
                case (_, True, _):  # Always include terminal characters
                    features.append(feature_vec)
                    labels.append(label)
                case (_, _, True):  # Sample some non-terminals based on rate
                    features.append(feature_vec)
                    labels.append(label)
                case _:  # Skip other non-terminal characters
                    pass

    def save(self, path: str, format: str = "skops", compress: bool = True, compression_level: int = 9) -> None:
        """
        Save the model and configuration to a file.

        Args:
            path (str): Path to save the model
            format (str, optional): Serialization format to use ('skops' or 'pickle'). 
                                    Defaults to 'skops' for secure serialization.
            compress (bool, optional): Whether to use compression. Defaults to True.
            compression_level (int, optional): Compression level (0-9, where 9 is highest).
                                              Defaults to 9.
        """
        if not self.is_trained:
            raise ValueError("Model has not been trained yet.")

        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)

        # Save all necessary information to recreate the model
        data = {
            "model": self.model,
            "encoder_cache": self.encoder.cache,
            "config": self.config,
            "version": 5,  # Version for backward compatibility (5 = with compression)
            "compressed": compress,
        }

        # Determine if we need to add a compression extension
        original_path = path
        compressed_path = None
        if compress and not (path.endswith('.xz') or path.endswith('.lzma')):
            compressed_path = path + '.xz'

        if format.lower() == "skops":
            # Use skops for secure serialization
            if compress:
                # Create a temporary buffer to hold the serialized data
                import io
                import lzma
                
                # Create a BytesIO buffer to hold the intermediate result
                buffer = io.BytesIO()
                
                # Serialize to the buffer using skops
                dump(data, buffer)
                
                # Get the serialized content
                buffer.seek(0)
                serialized_data = buffer.read()
                
                # Compress the serialized data using LZMA
                compressed_data = lzma.compress(serialized_data, preset=compression_level)
                
                # Write the compressed data to disk - use compressed_path if specified
                save_path = compressed_path if compressed_path else path
                with open(save_path, 'wb') as f:
                    f.write(compressed_data)
                    
                # Remove the uncompressed file if both paths exist and are different
                if compressed_path and os.path.exists(path) and path != save_path:
                    try:
                        os.remove(path)
                    except Exception:
                        pass  # Ignore errors when removing
            else:
                # Regular uncompressed saving
                dump(data, path)
        else:
            # Fallback to pickle format (less secure)
            if compress:
                import lzma
                # Use compressed_path if specified
                save_path = compressed_path if compressed_path else path
                with lzma.open(save_path, "wb", preset=compression_level) as f:
                    pickle.dump(data, f)
                    
                # Remove the uncompressed file if it exists
                if compressed_path and os.path.exists(path) and path != save_path:
                    try:
                        os.remove(path)
                    except Exception:
                        pass  # Ignore errors when removing
            else:
                with open(path, "wb") as f:
                    pickle.dump(data, f)

    @classmethod
    def load(cls, path: str, use_skops: bool = True, trust_model: bool = False) -> "TextSegmenter":
        """
        Load a model and configuration from a file.

        Args:
            path (str): Path to load the model from
            use_skops (bool, optional): Whether to use skops to load the model. Defaults to True.
            trust_model (bool, optional): Whether to trust all types in the model file. 
                                         Set to True only if you trust the source of the model file.
                                         Defaults to False.

        Returns:
            TextSegmenter: Loaded TextSegmenter instance
        """
        # Check for compression extensions and try alternative paths if needed
        original_path = path
        paths_to_try = [path]
        
        # If the path doesn't end with a compression extension, also try with extensions
        if not (path.endswith('.xz') or path.endswith('.lzma')):
            paths_to_try.append(path + '.xz')
            paths_to_try.append(path + '.lzma')
        
        # Keep track of the actual path that worked
        successful_path = None
        data = None
        last_exception = None
            
        # Try each path until one works
        for try_path in paths_to_try:
            if not os.path.exists(try_path):
                continue
                
            try:
                # Detect if file is compressed (looking at first few bytes)
                is_compressed = False
                with open(try_path, 'rb') as test_file:
                    # LZMA files start with 0xFD, '7', 'z', 'X', 'Z', 0x00
                    file_start = test_file.read(6)
                    if file_start.startswith(b'\xfd7zXZ\x00'):
                        is_compressed = True
                    
                if use_skops:
                    try:
                        if is_compressed:
                            # Handle compressed skops file
                            import io
                            import lzma
                            
                            # Read and decompress the file
                            with open(try_path, 'rb') as f:
                                compressed_data = f.read()
                                
                            # Decompress the data
                            decompressed_data = lzma.decompress(compressed_data)
                            
                            # Create a BytesIO buffer with the decompressed data
                            buffer = io.BytesIO(decompressed_data)
                            
                            # Load using skops
                            if trust_model:
                                # Trust all types in the file (use with caution)
                                from skops.io import get_untrusted_types
                                # Need a temporary file to get untrusted types
                                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                                    temp_file.write(decompressed_data)
                                    temp_file.flush()
                                    temp_path = temp_file.name
                                
                                try:
                                    # Get untrusted types from the temp file
                                    untrusted_types = get_untrusted_types(file=temp_path)
                                    buffer.seek(0)  # Reset buffer position
                                    data = load(buffer, trusted=untrusted_types)
                                finally:
                                    # Clean up temp file
                                    if os.path.exists(temp_path):
                                        os.remove(temp_path)
                            else:
                                data = load(buffer)
                                
                        else:
                            # Regular uncompressed skops file
                            if trust_model:
                                # Trust all types in the file (use with caution)
                                from skops.io import get_untrusted_types
                                untrusted_types = get_untrusted_types(file=try_path)
                                data = load(try_path, trusted=untrusted_types)
                            else:
                                # Only load trusted types
                                data = load(try_path)
                    except Exception as e:
                        if "UntrustedTypesFoundException" in str(e):
                            # Handle the specific case of untrusted types
                            print(f"Warning: Untrusted types found in model file. "
                                f"Attempting to load with untrusted types: {e}")
                            
                            # Try to load with untrusted types
                            from skops.io import get_untrusted_types
                            
                            if is_compressed:
                                # Need a temporary file to get untrusted types for compressed file
                                # Get the untrusted types using a temporary file
                                with open(try_path, 'rb') as f:
                                    compressed_data = f.read()
                                decompressed_data = lzma.decompress(compressed_data)
                                
                                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                                    temp_file.write(decompressed_data)
                                    temp_file.flush()
                                    temp_path = temp_file.name
                                
                                try:
                                    # Get untrusted types from the temp file
                                    untrusted_types = get_untrusted_types(file=temp_path)
                                    
                                    # Load with all types trusted (for default model)
                                    buffer = io.BytesIO(decompressed_data)
                                    data = load(buffer, trusted=untrusted_types)
                                finally:
                                    # Clean up temp file
                                    if os.path.exists(temp_path):
                                        os.remove(temp_path)
                            else:
                                untrusted_types = get_untrusted_types(file=try_path)
                                
                                # Register our custom types if possible
                                try:
                                    from skops.io import register_trusted_types
                                    # Import the specific types we need
                                    from charboundary.models import BinaryRandomForestModel
                                    register_trusted_types(BinaryRandomForestModel)
                                    register_trusted_types(SegmenterConfig)
                                except (ImportError, NameError):
                                    pass
                                
                                # Load with all types trusted (for default model)
                                data = load(try_path, trusted=untrusted_types)
                        else:
                            # Re-raise other exceptions
                            raise
                else:
                    # Fallback to pickle (less secure)
                    if is_compressed:
                        import lzma
                        with lzma.open(try_path, "rb") as f:
                            data = pickle.load(f)
                    else:
                        with open(try_path, "rb") as f:
                            data = pickle.load(f)
                            
                # If we reach here, we successfully loaded the data
                successful_path = try_path
                break
                    
            except Exception as e:
                last_exception = e
                continue
                
        # If we couldn't load from any path, raise the last exception
        if data is None:
            # If all paths fail, try pickle as fallback for backward compatibility
            print(f"Warning: Could not load model with specified method: {last_exception}")
            print("Attempting to load with pickle as fallback...")
            
            for try_path in paths_to_try:
                if not os.path.exists(try_path):
                    continue
                    
                try:
                    # Check if the file might be compressed
                    with open(try_path, 'rb') as test_file:
                        file_start = test_file.read(6)
                        
                    if file_start.startswith(b'\xfd7zXZ\x00'):
                        # LZMA compressed file
                        import lzma
                        with lzma.open(try_path, "rb") as f:
                            data = pickle.load(f)
                    else:
                        # Regular file
                        with open(try_path, "rb") as f:
                            data = pickle.load(f)
                            
                    successful_path = try_path
                    break
                except Exception as e:
                    last_exception = e
                    continue
                    
            if data is None:
                raise ValueError(f"Failed to load model from any of the candidate paths: {paths_to_try}. Last error: {last_exception}")

        encoder = CharacterEncoder()
        encoder.cache = data.get("encoder_cache", {})
        
        # Handle different versions
        version = data.get("version", 1)
        
        if version >= 4:
            # Version 4+ uses the config dataclass
            config = data.get("config", SegmenterConfig())
        else:
            # Older versions used individual parameters
            config = SegmenterConfig(
                left_window=data.get("left_window", 5),
                right_window=data.get("right_window", 5),
                abbreviations=data.get("abbreviations", DEFAULT_ABBREVIATIONS.copy()),
            )
        
        # Create the feature extractor
        feature_extractor = FeatureExtractor(
            encoder=encoder,
            abbreviations=config.abbreviations,
            use_numpy=config.use_numpy,
            cache_size=config.cache_size
        )
        
        segmenter = cls(
            model=data["model"],
            encoder=encoder,
            feature_extractor=feature_extractor,
            config=config,
        )

        return segmenter

    def segment_text(self, text: str) -> str:
        """
        Segment text into sentences and paragraphs.

        Args:
            text (str): Text to segment

        Returns:
            str: Text with sentence and paragraph annotations
        """
        if not self.is_trained:
            raise ValueError("Model has not been trained yet.")

        # Extract features for terminal characters only
        terminal_indices = []
        terminal_features = []
        
        for i, char in enumerate(text):
            if char in TERMINAL_SENTENCE_CHAR_LIST or char in TERMINAL_PARAGRAPH_CHAR_LIST:
                terminal_indices.append(i)
                char_features = self.feature_extractor.get_char_features(
                    text, self.config.left_window, self.config.right_window, positions=[i]
                )[0]
                terminal_features.append(char_features)
                
        # Only predict for terminal characters
        if terminal_features:
            predictions = self.model.predict(terminal_features)
        else:
            predictions = []
            
        # Apply segmentation
        result = list(text)
        
        # Insert tags from end to beginning to maintain correct indices
        # Sort indices in reverse order
        for idx, (pos, pred) in enumerate(zip(
            reversed(terminal_indices), 
            reversed(predictions)
        )):
            if pred == 1:
                char = text[pos]
                # Insert tags after this character
                insert_pos = pos + 1
                
                # Add paragraph tag for paragraph terminators (after sentence tag)
                if char in TERMINAL_PARAGRAPH_CHAR_LIST:
                    result.insert(insert_pos, PARAGRAPH_TAG)
                    
                # Add sentence tag for all boundaries
                result.insert(insert_pos, SENTENCE_TAG)
                
        return "".join(result)

    def segment_text_streaming(self, text: str, chunk_size: int = 10000, overlap: int = 100) -> Iterator[str]:
        """
        Memory-efficient streaming text segmentation.
        
        Args:
            text (str): Text to segment
            chunk_size (int, optional): Size of chunks to process at a time. Defaults to 10000.
            overlap (int, optional): Overlap between chunks to maintain context. Defaults to 100.
            
        Yields:
            Iterator[str]: Stream of segmented text fragments
        """
        if not self.is_trained:
            raise ValueError("Model has not been trained yet.")
            
        # For small texts, just use the regular segmenter
        if len(text) <= chunk_size:
            yield self.segment_text(text)
            return
            
        # Process text in overlapping chunks
        text_len = len(text)
        position = 0
        
        while position < text_len:
            # Calculate chunk bounds with overlap
            chunk_end = min(position + chunk_size, text_len)
            
            # Extract chunk with context
            if position > 0:
                # Ensure we have enough context for the first chunk
                context_start = max(0, position - overlap)
                chunk = text[context_start:chunk_end]
                context_len = position - context_start
            else:
                # First chunk has no left context
                chunk = text[position:chunk_end]
                context_len = 0
                
            # Add right context if not at the end
            if chunk_end < text_len:
                right_context_end = min(text_len, chunk_end + overlap)
                chunk += text[chunk_end:right_context_end]
                
            # Segment the chunk
            segmented_chunk = self.segment_text(chunk)
            
            # Remove context from the output
            if context_len > 0:
                # Find the first boundary after the context
                i = context_len
                while i < len(segmented_chunk) and not (
                    segmented_chunk[i:i+len(SENTENCE_TAG)] == SENTENCE_TAG or
                    segmented_chunk[i:i+len(PARAGRAPH_TAG)] == PARAGRAPH_TAG
                ):
                    i += 1
                    
                segmented_chunk = segmented_chunk[i:]
                
            # Find the position to cut off the right context
            if chunk_end < text_len:
                # Find the last boundary before the right context
                actual_chunk_len = chunk_end - position
                if context_len > 0:
                    actual_chunk_len = chunk_end - context_start
                    
                i = actual_chunk_len
                while i > 0 and not (
                    segmented_chunk[i-len(SENTENCE_TAG):i] == SENTENCE_TAG or
                    segmented_chunk[i-len(PARAGRAPH_TAG):i] == PARAGRAPH_TAG
                ):
                    i -= 1
                    
                if i > 0:
                    segmented_chunk = segmented_chunk[:i]
            
            # Yield the cleaned-up segmented chunk
            yield segmented_chunk
            
            # Move to the next chunk, accounting for any boundaries we found
            position = chunk_end

    def segment_to_sentences(self, text: str, streaming: bool = False) -> List[str]:
        """
        Segment text into a list of sentences.

        Args:
            text (str): Text to segment
            streaming (bool, optional): Whether to use streaming mode for memory efficiency.
                                       Defaults to False.

        Returns:
            List[str]: List of sentences
        """
        if streaming and len(text) > 10000:
            # For large texts, use streaming segmentation
            segmented_parts = list(self.segment_text_streaming(text))
            segmented_text = ''.join(segmented_parts)
        else:
            # For smaller texts, use regular segmentation
            segmented_text = self.segment_text(text)
            
        sentences = []
        current_sentence = []

        i = 0
        while i < len(segmented_text):
            if (i + len(SENTENCE_TAG) <= len(segmented_text) and
                    segmented_text[i:i + len(SENTENCE_TAG)] == SENTENCE_TAG):
                # Append the completed sentence
                if current_sentence:
                    sentences.append("".join(current_sentence))
                current_sentence = []
                i += len(SENTENCE_TAG)
            elif (i + len(PARAGRAPH_TAG) <= len(segmented_text) and
                  segmented_text[i:i + len(PARAGRAPH_TAG)] == PARAGRAPH_TAG):
                # Skip paragraph tags when extracting sentences
                i += len(PARAGRAPH_TAG)
            else:
                current_sentence.append(segmented_text[i])
                i += 1

        # Add the last sentence if there is one
        if current_sentence:
            sentences.append("".join(current_sentence))

        # Ensure each sentence is properly cleaned
        return [s.strip() for s in sentences if s.strip()]

    def segment_to_paragraphs(self, text: str, streaming: bool = False) -> List[str]:
        """
        Segment text into a list of paragraphs.

        Args:
            text (str): Text to segment
            streaming (bool, optional): Whether to use streaming mode for memory efficiency.
                                       Defaults to False.

        Returns:
            List[str]: List of paragraphs
        """
        if streaming and len(text) > 10000:
            # For large texts, use streaming segmentation
            segmented_parts = list(self.segment_text_streaming(text))
            segmented_text = ''.join(segmented_parts)
        else:
            # For smaller texts, use regular segmentation
            segmented_text = self.segment_text(text)
            
        paragraphs = []
        current_paragraph = []

        i = 0
        while i < len(segmented_text):
            if (i + len(PARAGRAPH_TAG) <= len(segmented_text) and
                    segmented_text[i:i + len(PARAGRAPH_TAG)] == PARAGRAPH_TAG):
                # Append the completed paragraph
                if current_paragraph:
                    paragraphs.append("".join(current_paragraph))
                current_paragraph = []
                i += len(PARAGRAPH_TAG)
            elif (i + len(SENTENCE_TAG) <= len(segmented_text) and
                  segmented_text[i:i + len(SENTENCE_TAG)] == SENTENCE_TAG):
                # Skip sentence tags when extracting paragraphs
                i += len(SENTENCE_TAG)
            else:
                current_paragraph.append(segmented_text[i])
                i += 1

        # Add the last paragraph if there is one
        if current_paragraph:
            paragraphs.append("".join(current_paragraph))

        # Ensure each paragraph is properly cleaned
        return [p.strip() for p in paragraphs if p.strip()]
        
    def get_abbreviations(self) -> List[str]:
        """
        Get the current list of abbreviations.
        
        Returns:
            List[str]: The current list of abbreviations
        """
        return sorted(list(self.config.abbreviations))
        
    def add_abbreviation(self, abbreviation: str) -> None:
        """
        Add a new abbreviation to the list.
        
        Args:
            abbreviation (str): The abbreviation to add (must end with a period)
        """
        if not abbreviation.endswith('.'):
            abbreviation = abbreviation + '.'
            
        # Update both the segmenter's abbreviation list and the feature extractor's
        self.config.abbreviations.append(abbreviation)
        self.feature_extractor.abbreviations.add(abbreviation)
        
    def remove_abbreviation(self, abbreviation: str) -> bool:
        """
        Remove an abbreviation from the list.
        
        Args:
            abbreviation (str): The abbreviation to remove
            
        Returns:
            bool: True if the abbreviation was removed, False if it wasn't in the list
        """
        if not abbreviation.endswith('.'):
            abbreviation = abbreviation + '.'
            
        if abbreviation in self.config.abbreviations:
            self.config.abbreviations.remove(abbreviation)
            if abbreviation in self.feature_extractor.abbreviations:
                self.feature_extractor.abbreviations.remove(abbreviation)
            return True
        return False
        
    def set_abbreviations(self, abbreviations: List[str]) -> None:
        """
        Set the complete list of abbreviations, replacing the current list.
        
        Args:
            abbreviations (List[str]): The new list of abbreviations
        """
        # Ensure all abbreviations end with periods
        self.config.abbreviations = [
            abbr if abbr.endswith('.') else abbr + '.' 
            for abbr in abbreviations
        ]
        
        # Update the feature extractor's abbreviations
        self.feature_extractor.abbreviations = set(self.config.abbreviations)

    def evaluate(
            self,
            data: Union[str, List[str]],
            max_samples: Optional[int] = None,
    ) -> MetricsResult:
        """
        Evaluate the model on a dataset.

        Args:
            data (Union[str, List[str]]):
                - Path to a test data file
                - List of annotated texts
            max_samples (int, optional): Maximum number of samples to process.
                If None, process all samples.

        Returns:
            MetricsResult: Evaluation metrics
        """
        if not self.is_trained:
            raise ValueError("Model has not been trained yet.")

        all_true_labels = []
        all_predictions = []

        # Process data
        if isinstance(data, str):
            # Path to a file
            if data.endswith('.jsonl.gz'):
                # Handle gzipped jsonl files
                with gzip.open(data, 'rt', encoding='utf-8') as f:
                    i = 0
                    for line in f:
                        if max_samples is not None and i >= max_samples:
                            break
                        try:
                            json_obj = json.loads(line.strip())
                            if 'text' in json_obj:
                                self._evaluate_text(json_obj['text'], all_true_labels, all_predictions)
                                i += 1
                        except json.JSONDecodeError:
                            print(f"Warning: Skipping invalid JSON line in {data}")
            else:
                # Handle regular text files
                with open(data, "r", encoding="utf-8") as input_file:
                    texts = input_file.readlines()
                    for i, text in enumerate(texts):
                        if max_samples is not None and i >= max_samples:
                            break
                        self._evaluate_text(text, all_true_labels, all_predictions)
        elif isinstance(data, list):
            for i, text in enumerate(data):
                if max_samples is not None and i >= max_samples:
                    break
                self._evaluate_text(text, all_true_labels, all_predictions)

        # Generate evaluation report
        report: MetricsResult = {
            "accuracy": 0.0,
            "boundary_accuracy": 0.0,
            "precision": 0.0,
            "recall": 0.0,
            "f1_score": 0.0,
            "binary_mode": True
        }
        
        if all_true_labels and all_predictions:
            # Calculate metrics
            accuracy = sklearn.metrics.accuracy_score(all_true_labels, all_predictions)
            
            # Classification report
            class_report = sklearn.metrics.classification_report(
                y_true=all_true_labels,
                y_pred=all_predictions,
                output_dict=True,
                zero_division=0
            )
            
            # Extract metrics for the boundary class (1)
            if "1" in class_report:
                precision = class_report["1"]["precision"]
                recall = class_report["1"]["recall"]
                f1_score = class_report["1"]["f1-score"]
            else:
                precision = 0.0
                recall = 0.0
                f1_score = 0.0
                
            # Update report
            report["accuracy"] = accuracy
            report["precision"] = precision
            report["recall"] = recall
            report["f1_score"] = f1_score
            
            # Also calculate boundary-specific metrics (on positions where either true or predicted is a boundary)
            boundary_indices = [i for i, (t, p) in enumerate(zip(all_true_labels, all_predictions)) 
                              if t == 1 or p == 1]
            
            if boundary_indices:
                boundary_true = [all_true_labels[i] for i in boundary_indices]
                boundary_pred = [all_predictions[i] for i in boundary_indices]
                boundary_accuracy = sklearn.metrics.accuracy_score(boundary_true, boundary_pred)
                report["boundary_accuracy"] = boundary_accuracy

        return report

    def _evaluate_text(
            self,
            text: str,
            all_true_labels: PositionLabels,
            all_predictions: PositionLabels,
    ) -> None:
        """
        Evaluate a text and add its true labels and predictions to the provided lists.

        Args:
            text (str): Annotated text
            all_true_labels (PositionLabels]): List to which true labels will be added
            all_predictions (PositionLabels]): List to which predictions will be added
        """
        clean_text, features, true_labels = self.feature_extractor.process_annotated_text(
            text, 
            self.config.left_window, 
            self.config.right_window,
            self.config.num_workers
        )

        predictions = self.model.predict(features)
        
        # Add all predictions and labels for proper evaluation
        all_true_labels.extend(true_labels)
        all_predictions.extend(predictions)