import pytest
from instantneo.skills.skill_decorators import skill
from typing import List, Dict, Any, Optional, Union

class TestSkillDecorator:
    """Pruebas para el decorador de skills."""
    
    def test_basic_skill_decoration(self):
        """Prueba la decoración básica de una skill."""
        @skill(description="Skill de prueba")
        def test_skill(param1: str, param2: int) -> str:
            """
            Una skill de prueba.
            
            Args:
                param1 (str): Primer parámetro.
                param2 (int): Segundo parámetro.
                
            Returns:
                str: Resultado de la skill.
            """
            return f"{param1}: {param2}"
        
        # Verificar que la función sigue siendo ejecutable
        result = test_skill("hello", 42)
        assert result == "hello: 42"
        
        # Verificar que se añadió la metadata
        assert hasattr(test_skill, "skill_metadata")
        assert test_skill.skill_metadata["name"] == "test_skill"
        assert test_skill.skill_metadata["description"] == "Skill de prueba"
        
        # Verificar los parámetros
        assert "param1" in test_skill.skill_metadata["parameters"]
        assert "param2" in test_skill.skill_metadata["parameters"]
        assert test_skill.skill_metadata["parameters"]["param1"]["type"] == "str"
        assert test_skill.skill_metadata["parameters"]["param2"]["type"] == "int"
    
    def test_auto_metadata_extraction(self):
        """Prueba la extracción automática de metadata desde docstrings."""
        @skill()  # Sin metadata explícita
        def auto_metadata_skill(name: str, age: int) -> str:
            """
            Skill con metadata extraída automáticamente.
            
            Args:
                name (str): Nombre de la persona.
                age (int): Edad de la persona.
                
            Returns:
                str: Un mensaje personalizado.
            """
            return f"Hola {name}, tienes {age} años."
        
        # Verificar que se extrajo la metadata del docstring
        assert auto_metadata_skill.skill_metadata["description"] == "Skill con metadata extraída automáticamente."
        assert auto_metadata_skill.skill_metadata["parameters"]["name"]["description"] == "Nombre de la persona."
        assert auto_metadata_skill.skill_metadata["parameters"]["age"]["description"] == "Edad de la persona."
    
    def test_required_parameters(self):
        """Prueba la detección de parámetros requeridos vs opcionales."""
        @skill()
        def skill_with_optional_params(required_param: str, optional_param: str = "default") -> str:
            """Skill con parámetros opcionales."""
            return f"{required_param} - {optional_param}"
        
        # Verificar que solo required_param está marcado como requerido
        assert "required_param" in skill_with_optional_params.skill_metadata["required"]
        assert "optional_param" not in skill_with_optional_params.skill_metadata["required"]
    
    def test_complex_parameter_types(self):
        """Prueba la extracción de tipos complejos de parámetros."""
        @skill()
        def complex_types_skill(
            string_list: List[str],
            dict_param: Dict[str, Any],
            optional_param: Optional[int] = None,
            union_param: Union[str, int] = "default"
        ) -> Dict[str, Any]:
            """Skill con tipos complejos."""
            return {"result": "ok"}
        
        # Verificar que se capturaron los tipos correctamente
        assert "string_list" in complex_types_skill.skill_metadata["parameters"]
        assert "dict_param" in complex_types_skill.skill_metadata["parameters"]
        assert "optional_param" in complex_types_skill.skill_metadata["parameters"]
        assert "union_param" in complex_types_skill.skill_metadata["parameters"]
        
        # Verificar que solo string_list y dict_param son requeridos
        assert "string_list" in complex_types_skill.skill_metadata["required"]
        assert "dict_param" in complex_types_skill.skill_metadata["required"]
        assert "optional_param" not in complex_types_skill.skill_metadata["required"]
        assert "union_param" not in complex_types_skill.skill_metadata["required"]
    
    def test_skill_with_tags(self):
        """Prueba la asignación de tags a skills."""
        @skill(tags=["math", "utility"])
        def tagged_skill(a: int, b: int) -> int:
            """Suma dos números."""
            return a + b
        
        # Verificar que se asignaron los tags correctamente
        assert "tags" in tagged_skill.skill_metadata
        assert "math" in tagged_skill.skill_metadata["tags"]
        assert "utility" in tagged_skill.skill_metadata["tags"]
    
    def test_skill_with_version(self):
        """Prueba la asignación de versión a skills."""
        @skill(version="2.0")
        def versioned_skill(param: str) -> str:
            """Skill con versión específica."""
            return param
        
        # Verificar que se asignó la versión correctamente
        assert "version" in versioned_skill.skill_metadata
        assert versioned_skill.skill_metadata["version"] == "2.0"
    
    def test_skill_with_custom_metadata(self):
        """Prueba la asignación de metadata personalizada a skills."""
        @skill(
            description="Skill personalizada",
            tags=["custom"],
            custom_field="valor personalizado",
            examples=[
                {"input": {"param": "test"}, "output": "test"}
            ]
        )
        def custom_skill(param: str) -> str:
            """Una skill con metadata personalizada."""
            return param
        
        # Verificar la metadata estándar
        assert custom_skill.skill_metadata["description"] == "Skill personalizada"
        assert "custom" in custom_skill.skill_metadata["tags"]
        
        # Verificar la metadata personalizada
        assert "custom_field" in custom_skill.skill_metadata
        assert custom_skill.skill_metadata["custom_field"] == "valor personalizado"
        assert "examples" in custom_skill.skill_metadata
        assert len(custom_skill.skill_metadata["examples"]) == 1
    
    def test_skill_with_explicit_parameters(self):
        """Prueba la asignación explícita de metadata de parámetros."""
        @skill(
            parameters={
                "param1": {
                    "type": "str",
                    "description": "Descripción personalizada",
                    "enum": ["opcion1", "opcion2"]
                },
                "param2": "Descripción simple"  # Formato simplificado
            }
        )
        def explicit_params_skill(param1: str, param2: int) -> str:
            """Skill con parámetros explícitos."""
            return f"{param1}: {param2}"
        
        # Verificar los parámetros explícitos
        params = explicit_params_skill.skill_metadata["parameters"]
        assert params["param1"]["description"] == "Descripción personalizada"
        assert "enum" in params["param1"]
        assert params["param1"]["enum"] == ["opcion1", "opcion2"]
        
        # Verificar el formato simplificado
        assert params["param2"]["description"] == "Descripción simple"
        # El tipo debería haberse inferido de las anotaciones
        assert params["param2"]["type"] == "int"
    
    def test_last_call_tracking(self):
        """Prueba el seguimiento de la última llamada a la skill."""
        @skill()
        def tracked_skill(param: str) -> str:
            """Skill con seguimiento de llamadas."""
            return f"Resultado: {param}"
        
        # Ejecutar la skill
        result = tracked_skill("test")
        assert result == "Resultado: test"
        
        # Verificar que se registró la llamada
        last_call = tracked_skill.get_last_call()
        assert last_call is not None
        assert last_call["args"] == ()
        assert last_call["kwargs"] == {"param": "test"}
        assert last_call["result"] == "Resultado: test"
        assert last_call["exception"] is None
        
        # Verificar los métodos auxiliares
        assert tracked_skill.get_last_result() == "Resultado: test"
        assert tracked_skill.get_last_params() == {"args": (), "kwargs": {"param": "test"}}
    
    def test_exception_tracking(self):
        """Prueba el seguimiento de excepciones en skills."""
        @skill()
        def error_skill(param: str) -> str:
            """Skill que lanza una excepción."""
            if param == "error":
                raise ValueError("Error de prueba")
            return f"Resultado: {param}"
        
        # Ejecutar la skill con éxito
        result = error_skill("ok")
        assert result == "Resultado: ok"
        
        # Ejecutar la skill con error
        with pytest.raises(ValueError) as excinfo:
            error_skill("error")
        
        assert "Error de prueba" in str(excinfo.value)
        
        # Verificar que se registró la excepción
        last_call = error_skill.get_last_call()
        assert last_call is not None
        assert last_call["args"] == ()
        assert last_call["kwargs"] == {"param": "error"}
        assert last_call["result"] is None
        assert isinstance(last_call["exception"], ValueError)
        assert str(last_call["exception"]) == "Error de prueba"

# Para ejecutar las pruebas:
# pytest test_skill_decorators.py -v