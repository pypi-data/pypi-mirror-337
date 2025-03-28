import pytest
from unittest.mock import patch, MagicMock
from instantneo.core import InstantNeo
from instantneo.skills.skill_decorators import skill

class TestIntegration:
    """Pruebas de integración para InstantNeo."""
    
    def test_basic_response(self, mock_instantneo):
        """Prueba la respuesta básica de InstantNeo."""
        result = mock_instantneo.run("Hola, ¿cómo estás?")
        assert result == "Respuesta simulada de OpenAI"
    
    def test_function_call(self, mock_instantneo_with_function):
        """Prueba la ejecución de function calls."""
        result = mock_instantneo_with_function.run("Suma 5 y 7")
        assert result == 12  # 5 + 7 = 12
    
    def test_streaming(self, mock_instantneo_streaming):
        """Prueba el streaming de respuestas."""
        chunks = []
        for chunk in mock_instantneo_streaming.run("Hola"):
            chunks.append(chunk)
        
        assert chunks == ["Hola", " mundo", "!"]
        assert "".join(chunks) == "Hola mundo!"
    
    def test_execution_modes(self, mock_instantneo_with_function):
        """Prueba los diferentes modos de ejecución."""
        # Modo WAIT_RESPONSE (por defecto)
        result = mock_instantneo_with_function.run("Suma 5 y 7")
        assert result == 12
        
        # Modo GET_ARGS
        result = mock_instantneo_with_function.run("Suma 5 y 7", execution_mode="get_args")
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["name"] == "suma"
        assert result[0]["arguments"] == {"a": 5, "b": 7}
        
        # Modo EXECUTION_ONLY
        result = mock_instantneo_with_function.run("Suma 5 y 7", execution_mode="execution_only")
        assert isinstance(result, str)
        assert "ejecutado" in result.lower() or "executed" in result.lower()
    
    def test_add_and_remove_skill(self, mock_instantneo):
        """Prueba la adición y eliminación de skills."""
        @skill(description="Skill de prueba")
        def test_skill(param: str) -> str:
            return f"Resultado: {param}"
        
        # Verificar que inicialmente no hay skills
        assert len(mock_instantneo.list_skills()) == 0
        
        # Añadir skill
        mock_instantneo.add_skill(test_skill)
        assert "test_skill" in mock_instantneo.list_skills()
        
        # Eliminar skill
        mock_instantneo.remove_skill("test_skill")
        assert "test_skill" not in mock_instantneo.list_skills()
    
    def test_role_setup(self):
        """Prueba la configuración del rol del sistema."""
        with patch('instantneo.adapters.openai_adapter.OpenAIAdapter') as mock_adapter:
            # Configurar el mock
            mock_adapter.return_value.create_chat_completion.return_value = MagicMock()
            mock_adapter.return_value.supports_images.return_value = True
            
            # Crear instancia con un rol específico
            role = "Eres un experto en Python"
            neo = InstantNeo(
                provider="openai",
                api_key="test_key",
                model="gpt-3.5-turbo",
                role_setup=role
            )
            
            # Ejecutar una consulta
            neo.run("Ayúdame con Python")
            
            # Verificar que se pasó el rol correctamente
            args, kwargs = mock_adapter.return_value.create_chat_completion.call_args
            assert "messages" in kwargs
            assert len(kwargs["messages"]) >= 2
            assert kwargs["messages"][0]["role"] == "system"
            assert kwargs["messages"][0]["content"] == role
    
    def test_override_params(self, mock_instantneo):
        """Prueba la anulación de parámetros en tiempo de ejecución."""
        # Configuración inicial
        assert mock_instantneo.config.model == "gpt-3.5-turbo"
        assert mock_instantneo.config.max_tokens == 200  # Valor por defecto
        
        # Ejecutar con parámetros anulados
        mock_instantneo.run(
            "Hola",
            model="gpt-4",
            max_tokens=100,
            temperature=0.7
        )
        
        # Verificar que se pasaron los parámetros anulados
        args, kwargs = mock_instantneo.adapter.create_chat_completion.call_args
        assert kwargs["model"] == "gpt-4"
        assert kwargs["max_tokens"] == 100
        assert kwargs["temperature"] == 0.7
        
        # Verificar que la configuración original no cambió
        assert mock_instantneo.config.model == "gpt-3.5-turbo"
        assert mock_instantneo.config.max_tokens == 200
    
    def test_return_full_response(self, mock_instantneo):
        """Prueba la opción de devolver la respuesta completa."""
        # Respuesta normal (solo contenido)
        result = mock_instantneo.run("Hola")
        assert result == "Respuesta simulada de OpenAI"
        
        # Respuesta completa
        full_result = mock_instantneo.run("Hola", return_full_response=True)
        assert isinstance(full_result, dict) or hasattr(full_result, "choices")
        
        if isinstance(full_result, dict):
            assert "choices" in full_result
        else:
            assert hasattr(full_result, "choices")
    
    @pytest.mark.skipif(not os.path.exists(".env"), reason="No .env file for API keys")
    def test_real_api_integration(self, real_instantneo):
        """
        Prueba la integración con la API real.
        Esta prueba se omite si no hay un archivo .env con API keys.
        """
        result = real_instantneo.run("¿Cuál es la capital de Francia?")
        assert result and isinstance(result, str)
        assert "París" in result or "Paris" in result
    
    def test_multiple_skills(self, mock_instantneo, test_skills):
        """Prueba el uso de múltiples skills."""
        # Registrar varias skills
        for skill_func in test_skills.values():
            mock_instantneo.add_skill(skill_func)
        
        # Verificar que todas las skills están registradas
        registered_skills = mock_instantneo.list_skills()
        for skill_name in test_skills.keys():
            assert skill_name in registered_skills
        
        # Verificar que se pueden filtrar skills por tag
        skills_by_tag = mock_instantneo.skill_manager.get_skills_by_tag("text")
        assert "concatenar" in skills_by_tag
        
        skills_by_tag = mock_instantneo.skill_manager.get_skills_by_tag("filter")
        assert "filtrar" in skills_by_tag

# Pruebas específicas para imágenes
class TestImageIntegration:
    """Pruebas de integración para el procesamiento de imágenes."""
    
    def test_image_processing_url(self):
        """Prueba el procesamiento de imágenes desde URL."""
        with patch('instantneo.adapters.openai_adapter.OpenAIAdapter') as mock_adapter:
            # Configurar el mock
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message = MagicMock()
            mock_response.choices[0].message.content = "Descripción de la imagen"
            
            mock_adapter.return_value.supports_images.return_value = True
            mock_adapter.return_value.create_chat_completion.return_value = mock_response
            
            # Crear instancia con imagen
            image_url = "https://example.com/image.jpg"
            neo = InstantNeo(
                provider="openai",
                api_key="test_key",
                model="gpt-4-vision-preview",
                role_setup="Describe esta imagen",
                images=image_url
            )
            
            # Ejecutar
            result = neo.run("¿Qué ves en esta imagen?")
            
            # Verificar que se procesó correctamente
            assert result == "Descripción de la imagen"
            
            # Verificar que se llamó al método con la imagen procesada
            args, kwargs = mock_adapter.return_value.create_chat_completion.call_args
            assert "messages" in kwargs
            assert len(kwargs["messages"]) > 0
            assert "content" in kwargs["messages"][1]
            
            # Si el contenido es una lista (formato multimodal)
            if isinstance(kwargs["messages"][1]["content"], list):
                assert len(kwargs["messages"][1]["content"]) > 1  # Texto + imagen
                assert kwargs["messages"][1]["content"][0]["type"] == "text"
                assert kwargs["messages"][1]["content"][1]["type"] == "image_url"
                assert kwargs["messages"][1]["content"][1]["image_url"]["url"] == image_url
    
    def test_multiple_images(self):
        """Prueba el procesamiento de múltiples imágenes."""
        with patch('instantneo.adapters.openai_adapter.OpenAIAdapter') as mock_adapter:
            # Configurar el mock
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message = MagicMock()
            mock_response.choices[0].message.content = "Descripción de las imágenes"
            
            mock_adapter.return_value.supports_images.return_value = True
            mock_adapter.return_value.create_chat_completion.return_value = mock_response
            
            # Crear instancia con múltiples imágenes
            image_urls = [
                "https://example.com/image1.jpg",
                "https://example.com/image2.jpg"
            ]
            neo = InstantNeo(
                provider="openai",
                api_key="test_key",
                model="gpt-4-vision-preview",
                role_setup="Describe estas imágenes",
                images=image_urls
            )
            
            # Ejecutar
            result = neo.run("¿Qué ves en estas imágenes?")
            
            # Verificar que se procesó correctamente
            assert result == "Descripción de las imágenes"
            
            # Verificar que se llamó al método con las imágenes procesadas
            args, kwargs = mock_adapter.return_value.create_chat_completion.call_args
            assert "messages" in kwargs
            
            # Si el contenido es una lista (formato multimodal)
            if isinstance(kwargs["messages"][1]["content"], list):
                # Debería haber 3 elementos: texto + 2 imágenes
                assert len(kwargs["messages"][1]["content"]) == 3
                assert kwargs["messages"][1]["content"][0]["type"] == "text"
                assert kwargs["messages"][1]["content"][1]["type"] == "image_url"
                assert kwargs["messages"][1]["content"][2]["type"] == "image_url"
                assert kwargs["messages"][1]["content"][1]["image_url"]["url"] == image_urls[0]
                assert kwargs["messages"][1]["content"][2]["image_url"]["url"] == image_urls[1]
    
    def test_image_detail_level(self):
        """Prueba diferentes niveles de detalle de imagen."""
        with patch('instantneo.adapters.openai_adapter.OpenAIAdapter') as mock_adapter:
            # Configurar el mock
            mock_adapter.return_value.supports_images.return_value = True
            mock_adapter.return_value.create_chat_completion.return_value = MagicMock()
            
            # Crear instancia con nivel de detalle específico
            image_url = "https://example.com/image.jpg"
            neo = InstantNeo(
                provider="openai",
                api_key="test_key",
                model="gpt-4-vision-preview",
                role_setup="Describe esta imagen",
                images=image_url,
                image_detail="high"  # Nivel de detalle alto
            )
            
            # Ejecutar
            neo.run("¿Qué ves en esta imagen?")
            
            # Verificar que se pasó el nivel de detalle
            args, kwargs = mock_adapter.return_value.create_chat_completion.call_args
            
            # Si el contenido es una lista (formato multimodal)
            if isinstance(kwargs["messages"][1]["content"], list):
                for item in kwargs["messages"][1]["content"]:
                    if item["type"] == "image_url" and "detail" in item["image_url"]:
                        assert item["image_url"]["detail"] == "high"

# Para ejecutar las pruebas:
# pytest test_integration.py -v