import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.constants import NEXUS, PROBE, PYLON, ASSIMILATOR


class StevenBot(sc2.BotAI):
    async def on_step(self, iteration):
        await self.distribute_workers()
        await self.build_workers()
        await self.build_pylons()
        await self.build_assimilators()
        await self.expand()

    async def build_workers(self):
        for nexus in self.units(NEXUS).ready.noqueue:
            if self.can_afford(PROBE):
                await self.do(nexus.train(PROBE))

    async def build_pylons(self):
        if self.supply_left < 5 and not self.already_pending(PYLON):
            nexuses = self.units(NEXUS).ready
            if nexuses.exists:
                if self.can_afford(PYLON):
                    await self.build(PYLON, near = nexuses.first)

    async def build_assimilators(self):
        for nexus in self.units(NEXUS).ready:
            vaspenes = self.state.vespene_geyser.closer_than(15.0, nexus)
            for vesp in vaspenes:
                if not self.can_afford(ASSIMILATOR):
                    break
                worker = self.select_build_worker(vesp.position)
                if worker is None:
                    break
                if not self.units(ASSIMILATOR).closer_than(1.0, vesp).exists:
                    await self.do(worker.build(ASSIMILATOR, vesp))

    async def expand(self):
        if self.units(NEXUS).amount < 3 and self.can_afford(NEXUS):
            await self.expand_now()


run_game(maps.get("AbyssalReefLE"), [
    Bot(Race.Protoss, StevenBot()),
    Computer(Race.Terran, Difficulty.Easy)
    ], realtime=False)