import pytest
import os
import tempfile
import base64
from unittest.mock import patch, mock_open
from instantneo.utils.image_utils import is_url, get_media_type_from_extension, encode_image_to_base64, process_images
from instantneo.utils.skill_utils import python_type_to_string, format_tool

class TestImageUtils:
    """Pruebas para las utilidades de procesamiento de imágenes."""
    
    def test_is_url(self):
        """Prueba la detección de URLs."""
        assert is_url("https://example.com/image.jpg") is True
        assert is_url("http://example.com") is True
        assert is_url("file:///path/to/file.jpg") is True
        assert is_url("path/to/file.jpg") is False
        assert is_url("") is False
    
    def test_get_media_type(self):
        """Prueba la determinación del tipo de medio basado en la extensión."""
        assert get_media_type_from_extension("image.jpg") == "image/jpeg"
        assert get_media_type_from_extension("image.jpeg") == "image/jpeg"
        assert get_media_type_from_extension("image.png") == "image/png"
        assert get_media_type_from_extension("image.gif") == "image/gif"
        assert get_media_type_from_extension("image.webp") == "image/webp"
        
        with pytest.raises(ValueError):
            get_media_type_from_extension("image.txt")
    
    def test_encode_image_to_base64(self):
        """Prueba la codificación de imágenes a base64."""
        # Crear un archivo temporal con datos de prueba
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(b"test image data")
            temp_path = temp_file.name
        
        try:
            # Mockear la función open para evitar leer el archivo real
            with patch("builtins.open", mock_open(read_data=b"test image data")):
                encoded = encode_image_to_base64(temp_path)
                # Verificar que el resultado es una cadena base64 válida
                assert isinstance(encoded, str)
                # Decodificar y verificar que los datos son correctos
                decoded = base64.b64decode(encoded).decode('utf-8')
                assert decoded == "test image data"
        finally:
            # Limpiar
            os.unlink(temp_path)
    
    def test_process_images_url(self):
        """Prueba el procesamiento de imágenes desde URL."""
        url = "https://example.com/image.jpg"
        result = process_images(url, "auto")
        
        assert len(result) == 1
        assert result[0]["type"] == "image_url"
        assert result[0]["image_url"]["url"] == url
    
    def test_process_images_multiple_urls(self):
        """Prueba el procesamiento de múltiples URLs de imágenes."""
        urls = ["https://example.com/image1.jpg", "https://example.com/image2.png"]
        result = process_images(urls, "auto")
        
        assert len(result) == 2
        assert result[0]["type"] == "image_url"
        assert result[0]["image_url"]["url"] == urls[0]
        assert result[1]["type"] == "image_url"
        assert result[1]["image_url"]["url"] == urls[1]
    
    def test_process_images_local_file(self):
        """Prueba el procesamiento de imágenes locales."""
        # Crear un archivo temporal con datos de prueba
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
            temp_file.write(b"test image data")
            temp_path = temp_file.name
        
        try:
            # Mockear la función encode_image_to_base64
            with patch("instantneo.utils.image_utils.encode_image_to_base64", return_value="base64encodeddata"):
                result = process_images(temp_path, "auto")
                
                assert len(result) == 1
                assert result[0]["type"] == "image_url"
                assert "data:image/jpeg;base64,base64encodeddata" in result[0]["image_url"]["url"]
        finally:
            # Limpiar
            os.unlink(temp_path)

class TestSkillUtils:
    """Pruebas para las utilidades de skills."""
    
    def test_python_type_to_string(self):
        """Prueba la conversión de tipos Python a strings."""
        assert python_type_to_string(int) == "integer"
        assert python_type_to_string(float) == "number"
        assert python_type_to_string(str) == "string"
        assert python_type_to_string(bool) == "boolean"
        assert python_type_to_string(list) == "array"
        assert python_type_to_string(dict) == "object"
        assert python_type_to_string("int") == "integer"
        assert python_type_to_string("float") == "number"
        assert python_type_to_string("str") == "string"
        assert python_type_to_string("bool") == "boolean"
        assert python_type_to_string("list") == "array"
        assert python_type_to_string("dict") == "object"
        assert python_type_to_string("unknown") == "string"  # Tipo desconocido
    
    def test_format_tool_basic(self):
        """Prueba el formateo básico de una herramienta."""
        skill_info = {
            "name": "test_skill",
            "description": "A test skill",
            "parameters": {
                "param1": {
                    "type": "str",
                    "description": "A string parameter"
                },
                "param2": {
                    "type": "int",
                    "description": "An integer parameter"
                }
            },
            "required": ["param1"]
        }
        
        result = format_tool(skill_info)
        
        assert result["type"] == "function"
        assert result["function"]["name"] == "test_skill"
        assert result["function"]["description"] == "A test skill"
        assert result["function"]["parameters"]["type"] == "object"
        assert result["function"]["parameters"]["properties"]["param1"]["type"] == "string"
        assert result["function"]["parameters"]["properties"]["param2"]["type"] == "integer"
        assert result["function"]["parameters"]["required"] == ["param1"]
    
    def test_format_tool_with_enum(self):
        """Prueba el formateo de una herramienta con valores enum."""
        skill_info = {
            "name": "weather",
            "description": "Get weather information",
            "parameters": {
                "location": {
                    "type": "str",
                    "description": "City name",
                },
                "unit": {
                    "type": "str",
                    "description": "Temperature unit",
                    "enum": ["celsius", "fahrenheit"]
                }
            },
            "required": ["location"]
        }
        
        result = format_tool(skill_info)
        
        assert result["function"]["parameters"]["properties"]["unit"]["enum"] == ["celsius", "fahrenheit"]
    
    def test_format_tool_complex_types(self):
        """Prueba el formateo de una herramienta con tipos complejos."""
        skill_info = {
            "name": "complex_skill",
            "description": "A skill with complex types",
            "parameters": {
                "array_param": {
                    "type": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "description": "An array parameter"
                },
                "object_param": {
                    "type": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "age": {"type": "integer"}
                        }
                    },
                    "description": "An object parameter"
                }
            },
            "required": []
        }
        
        result = format_tool(skill_info)
        
        # Verificar el parámetro de tipo array
        array_param = result["function"]["parameters"]["properties"]["array_param"]
        assert array_param["type"] == "array"
        assert array_param["items"]["type"] == "string"
        
        # Verificar el parámetro de tipo object
        object_param = result["function"]["parameters"]["properties"]["object_param"]
        assert object_param["type"] == "object"
        assert object_param["properties"]["name"]["type"] == "string"
        assert object_param["properties"]["age"]["type"] == "integer"
    
    def test_format_tool_missing_parameters(self):
        """Prueba el formateo de una herramienta con parámetros faltantes."""
        skill_info = {
            "name": "incomplete_skill",
            "description": "A skill with missing parameters"
            # Falta el campo 'parameters'
        }
        
        with pytest.raises(ValueError) as excinfo:
            format_tool(skill_info)
        
        assert "missing 'parameters' key" in str(excinfo.value)

# Para ejecutar las pruebas:
# pytest test_utils.py -v