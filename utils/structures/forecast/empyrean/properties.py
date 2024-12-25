from typing import Any, Self


class EmpyreanProperties():

    class Keys():
        name: str       = "name"
        isDaytime: str  = "isDaytime"
        icon: str       = "icon"
    
    def __init__(self) -> None:
        self.name: str = ""
        self.isDaytime: bool = False
        self.icon: str = ""
    
    @staticmethod
    def from_API(properties: dict[str, Any]) -> Self:
        new_instance = EmpyreanProperties()
        new_instance.name = properties[EmpyreanProperties.Keys.name]
        new_instance.isDaytime = bool(properties[EmpyreanProperties.Keys.isDaytime])
        new_instance.icon = properties[EmpyreanProperties.Keys.icon] #TODO :: Convert API link of icon to local path
        return new_instance
    
    @staticmethod
    def from_Empyrean(properties: dict[str, Any]) -> Self:
        new_instance = EmpyreanProperties()
        new_instance.name = properties[EmpyreanProperties.Keys.name]
        new_instance.isDaytime = bool(properties[EmpyreanProperties.Keys.isDaytime])
        new_instance.icon = properties[EmpyreanProperties.Keys.icon]
        return new_instance

    def to_dict(self) -> dict[str, str]:
        return {
            EmpyreanProperties.Keys.name : self.name,
            EmpyreanProperties.Keys.isDaytime : str(self.isDaytime),
            EmpyreanProperties.Keys.icon : self.icon
        }
