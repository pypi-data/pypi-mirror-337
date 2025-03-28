import pytest
from instantneo.skills.skill_manager import SkillManager
from instantneo.skills.skill_decorators import skill
from instantneo.skills.skill_manager_operations import SkillManagerOperations
import tempfile
import os

# Fixture para SkillManager
@pytest.fixture
def skill_manager():
    return SkillManager()

# Pruebas de registro y recuperación de skills
def test_skill_registration(skill_manager):
    """Prueba el registro y recuperación de skills."""
    
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
    
    # Registrar la skill
    skill_manager.register_skill(test_skill)
    
    # Verificar que la skill se registró correctamente
    assert "test_skill" in skill_manager.get_skill_names()
    
    # Verificar que se puede recuperar la skill
    retrieved_skill = skill_manager.get_skill_by_name("test_skill")
    assert retrieved_skill is not None
    assert retrieved_skill.__name__ == "test_skill"
    
    # Verificar la metadata
    metadata = skill_manager.get_skill_metadata_by_name("test_skill")
    assert metadata is not None
    assert metadata["description"] == "Skill de prueba"
    assert "param1" in metadata["parameters"]
    assert "param2" in metadata["parameters"]
    
    # Verificar que la skill es ejecutable
    result = retrieved_skill("hello", 42)
    assert result == "hello: 42"

def test_skill_metadata_extraction(skill_manager):
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
    
    skill_manager.register_skill(auto_metadata_skill)
    
    # Verificar la metadata extraída automáticamente
    metadata = skill_manager.get_skill_metadata_by_name("auto_metadata_skill")
    assert metadata["description"] == "Skill con metadata extraída automáticamente."
    assert "name" in metadata["parameters"]
    assert "age" in metadata["parameters"]
    assert metadata["parameters"]["name"]["description"] == "Nombre de la persona."
    assert metadata["parameters"]["age"]["description"] == "Edad de la persona."
    assert metadata["parameters"]["name"]["type"] == "str"
    assert metadata["parameters"]["age"]["type"] == "int"

def test_skill_with_tags(skill_manager):
    """Prueba el registro de skills con tags y su recuperación por tag."""
    
    @skill(description="Skill con tags", tags=["math", "utility"])
    def math_skill(a: int, b: int) -> int:
        """Suma dos números."""
        return a + b
    
    skill_manager.register_skill(math_skill)
    
    # Verificar recuperación por tag
    math_skills = skill_manager.get_skills_by_tag("math")
    assert "math_skill" in math_skills
    
    utility_skills = skill_manager.get_skills_by_tag("utility")
    assert "math_skill" in utility_skills
    
    # Verificar que no aparece en tags que no tiene
    other_skills = skill_manager.get_skills_by_tag("other")
    assert "math_skill" not in other_skills

def test_skill_removal(skill_manager):
    """Prueba la eliminación de skills."""
    
    @skill(description="Skill para eliminar")
    def temp_skill(x: int) -> int:
        return x * 2
    
    skill_manager.register_skill(temp_skill)
    assert "temp_skill" in skill_manager.get_skill_names()
    
    # Eliminar la skill
    result = skill_manager.remove_skill("temp_skill")
    assert result is True
    
    # Verificar que ya no está en el registro
    assert "temp_skill" not in skill_manager.get_skill_names()
    
    # Intentar eliminar una skill que no existe
    result = skill_manager.remove_skill("non_existent_skill")
    assert result is False

# Pruebas de operaciones de SkillManager
def test_skill_manager_union():
    """Prueba la unión de dos SkillManagers."""
    
    # Crear dos managers con skills diferentes
    manager1 = SkillManager()
    manager2 = SkillManager()
    
    @skill(description="Skill 1")
    def skill1(param: str) -> str:
        return param
    
    @skill(description="Skill 2")
    def skill2(param: int) -> int:
        return param
    
    manager1.register_skill(skill1)
    manager2.register_skill(skill2)
    
    # Unir los managers
    union_manager = SkillManagerOperations.union(manager1, manager2)
    
    # Verificar que el manager unión contiene ambas skills
    assert "skill1" in union_manager.get_skill_names()
    assert "skill2" in union_manager.get_skill_names()
    
    # Verificar que las skills son ejecutables
    skill1_instance = union_manager.get_skill_by_name("skill1")
    skill2_instance = union_manager.get_skill_by_name("skill2")
    
    assert skill1_instance("test") == "test"
    assert skill2_instance(42) == 42

def test_skill_manager_intersection():
    """Prueba la intersección de dos SkillManagers."""
    
    # Crear dos managers con algunas skills en común
    manager1 = SkillManager()
    manager2 = SkillManager()
    
    @skill(description="Skill común")
    def common_skill(param: str) -> str:
        return param
    
    @skill(description="Skill solo en manager1")
    def skill1(param: str) -> str:
        return param
    
    @skill(description="Skill solo en manager2")
    def skill2(param: int) -> int:
        return param
    
    manager1.register_skill(common_skill)
    manager1.register_skill(skill1)
    
    manager2.register_skill(common_skill)
    manager2.register_skill(skill2)
    
    # Obtener la intersección
    intersection_manager = SkillManagerOperations.intersection(manager1, manager2)
    
    # Verificar que solo contiene la skill común
    assert "common_skill" in intersection_manager.get_skill_names()
    assert "skill1" not in intersection_manager.get_skill_names()
    assert "skill2" not in intersection_manager.get_skill_names()
    
    # Verificar que la skill es ejecutable
    common = intersection_manager.get_skill_by_name("common_skill")
    assert common("test") == "test"

def test_skill_manager_difference():
    """Prueba la diferencia entre dos SkillManagers."""
    
    # Crear dos managers con algunas skills en común
    manager1 = SkillManager()
    manager2 = SkillManager()
    
    @skill(description="Skill común")
    def common_skill(param: str) -> str:
        return param
    
    @skill(description="Skill solo en manager1")
    def skill1(param: str) -> str:
        return param
    
    @skill(description="Skill solo en manager2")
    def skill2(param: int) -> int:
        return param
    
    manager1.register_skill(common_skill)
    manager1.register_skill(skill1)
    
    manager2.register_skill(common_skill)
    manager2.register_skill(skill2)
    
    # Obtener la diferencia (skills en manager1 pero no en manager2)
    diff_manager = SkillManagerOperations.difference(manager1, manager2)
    
    # Verificar que solo contiene skill1
    assert "skill1" in diff_manager.get_skill_names()
    assert "common_skill" not in diff_manager.get_skill_names()
    assert "skill2" not in diff_manager.get_skill_names()

def test_skill_manager_compare():
    """Prueba la comparación de dos SkillManagers."""
    
    # Crear dos managers con algunas skills en común
    manager1 = SkillManager()
    manager2 = SkillManager()
    
    @skill(description="Skill común")
    def common_skill(param: str) -> str:
        return param
    
    @skill(description="Skill solo en manager1")
    def skill1(param: str) -> str:
        return param
    
    @skill(description="Skill solo en manager2")
    def skill2(param: int) -> int:
        return param
    
    manager1.register_skill(common_skill)
    manager1.register_skill(skill1)
    
    manager2.register_skill(common_skill)
    manager2.register_skill(skill2)
    
    # Comparar los managers
    comparison = SkillManagerOperations.compare(manager1, manager2)
    
    # Verificar los resultados
    assert "common_skill" in comparison["common_skills"]
    assert "skill1" in comparison["unique_to_a"]
    assert "skill2" in comparison["unique_to_b"]
    assert len(comparison["common_skills"]) == 1
    assert len(comparison["unique_to_a"]) == 1
    assert len(comparison["unique_to_b"]) == 1

# Para ejecutar las pruebas:
# pytest test_skill_manager.py -v