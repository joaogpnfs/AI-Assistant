import enum
import datetime
from typing import Annotated
from livekit.agents import llm
import logging

logger = logging.getLogger("temperature-control")
logger.setLevel(logging.INFO)

class Zone(enum.Enum):
  LIVING_ROOM = "living_room"
  BEDROOM = "bedroom"
  KITCHEN = "kitchen"
  BATHROOM = "bathroom"
  OFFICE = "office"
  
class AssistantFnc(llm.FunctionContext):
  def __init__(self) -> None:
    super().__init__()
    
    self._temperature = {
      Zone.LIVING_ROOM: 20,
      Zone.BEDROOM: 20,
      Zone.KITCHEN: 24,
      Zone.BATHROOM: 23,
      Zone.OFFICE: 21,
    }
  
  @llm.ai_callable(description="Get the current temperature in a specific zone")
  def get_temperature(self, zone: Annotated[Zone, llm.TypeInfo(description="The specific zone to get the temperature for")]):
    logger.info("get temp - zone %s", zone)
    temp = self._temperature[Zone(zone)]
    return f"The temperature in the {zone} is {temp}°C"
  
  @llm.ai_callable(description="Set the temperature in a specific zone")
  def set_temperature(
        self, 
        zone: Annotated[Zone, llm.TypeInfo(description="The specific zone to set the temperature for")], 
        temperature: Annotated[float, llm.TypeInfo(description="The temperature to set in the zone")]):
    
    logger.info("set temp - zone %s, temp %s", zone, temperature)
    self._temperature[Zone(zone)] = temperature
    return f"The temperature in the {zone} has been set to {temperature}°C"
  
  @llm.ai_callable(description="Get the current time")
  def get_time(self):
    logger.info("get time")
    return f"The current time is {datetime.datetime.now().strftime('%H:%M:%S')}"

  @llm.ai_callable(description="Get the current date")
  def get_date(self):
    logger.info("get date")
    return f"The current date is {datetime.datetime.now().strftime('%Y-%m-%d')}"
  
