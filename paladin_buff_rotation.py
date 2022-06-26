# https://www.playlostark.com/en-us/game/classes/warrior/paladin
# Context: Both abilities apply the same damage buff so they should not be applied at the same time

# Given Wrath of God, Heavenly Blessings cooldowns and running time in seconds
# Returns the optimal rotation of buffs for maximum uptime over the running time

# in the optimal rotation, buffs are applied as soon as possible

from typing import List
import functools

WRATH_OF_GOD_BUFF_DURATION_SECONDS = 7
HEAVENLY_BLESSINGS_BUFF_DURATION_SECONDS = 7

class BuffInterval:
  def __init__(self, buff_name, starts_at, ends_at) -> None:
    self.buff_name = buff_name
    self.starts_at = starts_at
    self.ends_at = ends_at
  
  def __str__(self) -> str:
    return f"{self.buff_name}:[{self.starts_at},{self.ends_at}]"
  
  def __repr__(self):
    return str(self)

class BuffTimeline:
  def __init__(self, timeline: List[BuffInterval]=list()) -> None:
    self.timeline = timeline

  def __str__(self) -> str:
    return str(self.timeline)

  def __repr__(self):
    return str(self)
  
  def __add__(self, interval: BuffInterval):
    return BuffTimeline(self.timeline + [interval])

  def buff_uptime(self) -> int:
    return functools.reduce(lambda accumulator, interval: accumulator + (interval.ends_at - interval.starts_at), self.timeline, 0)

def paladin_buff_rotation(
  wrath_of_god_cd: int,
  heavenly_bessings_cd: int,
  running_time: int,
  all_outcomes: List[BuffTimeline],
  buff_timeline: BuffTimeline=BuffTimeline(),
  current_time: int=0,
  wrath_of_god_available_at: int=0,
  heavenly_blessings_available_at: int=0,
) -> None:

  if running_time <= current_time:
    all_outcomes.append(buff_timeline)
    return

  wrath_of_god_available = wrath_of_god_available_at <= current_time
  heavenly_blessings_available = heavenly_blessings_available_at <= current_time

  if wrath_of_god_available:
    buff_ends_at = min(running_time, current_time + WRATH_OF_GOD_BUFF_DURATION_SECONDS)
    paladin_buff_rotation(
      wrath_of_god_cd,
      heavenly_bessings_cd,
      running_time,
      all_outcomes,
      buff_timeline + BuffInterval("WOG", current_time, buff_ends_at),
      buff_ends_at,
      current_time + wrath_of_god_cd,
      heavenly_blessings_available_at,
    )

  if heavenly_blessings_available:
    buff_ends_at = min(running_time, current_time + HEAVENLY_BLESSINGS_BUFF_DURATION_SECONDS)
    paladin_buff_rotation(
      wrath_of_god_cd,
      heavenly_bessings_cd,
      running_time,
      all_outcomes,
      buff_timeline + BuffInterval("HB", current_time, buff_ends_at),
      buff_ends_at,
      wrath_of_god_available_at,
      current_time + heavenly_bessings_cd,
    )

  if not wrath_of_god_available and not heavenly_blessings_available:
    next_buff_available_at = min(wrath_of_god_available_at, heavenly_blessings_available_at)
    paladin_buff_rotation(
      wrath_of_god_cd,
      heavenly_bessings_cd,
      running_time,
      all_outcomes,
      buff_timeline,
      next_buff_available_at,
      wrath_of_god_available_at,
      heavenly_blessings_available_at,
    )

all_outcomes = []
running_time = 3000

paladin_buff_rotation(17, 22, running_time, all_outcomes)

all_outcomes.sort(key=lambda timeline: timeline.buff_uptime(), reverse=True) 

for timeline in all_outcomes:
  print(f"{timeline.buff_uptime()}/{running_time} {timeline.timeline[0:10]}")