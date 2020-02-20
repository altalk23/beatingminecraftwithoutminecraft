from nbt.nbt import *
from nbt.region import *
from os import mkdir

# So welcome to terrible code I guess

# Pos of player — Needed for this
pos = TAG_List(name='Pos', type=TAG_Double)
pos.extend([
    TAG_Double(value=0.5),
    TAG_Double(value=100),
    TAG_Double(value=0.5),
])

# Rotation of player — Not needed for this, purely aesthetical
rotation = TAG_List(name='Rotation', type=TAG_Float)
rotation.extend([
    TAG_Float(value=0),
    TAG_Float(value=90),
])

# Player — A lot of tags missing, not needed
player = TAG_Compound()
player.name = 'Player'
player.tags.extend([
    TAG_Int(name='Dimension', value=1),
    TAG_Int(name='PlayerGameType', value=1),
    rotation,
    pos,
])

# Dragon fight data — Needed for this
dragonfight = TAG_Compound()
dragonfight.name = 'DragonFight'
dragonfight.tags.extend([
    TAG_Byte(name='DragonKilled', value=1),
    TAG_Byte(name='PreviouslyKilled', value=1),
])

# Nesting
one = TAG_Compound()
one.name = '1'
one.tags.append(dragonfight)

# Nesting
dimensiondata = TAG_Compound()
dimensiondata.name = 'DimensionData'
dimensiondata.tags.append(one)

# Level.dat data — Necessary stuff + 69's
data = TAG_Compound()
data.name = 'Data'
data.tags.extend([
    TAG_String(name='LevelName', value='Beating Minecraft Without Minecraft'),
    TAG_Byte(name='initialized', value=1),
    TAG_Int(name='version', value=19133),
    TAG_Int(name='SpawnY', value=69),
    TAG_Long(name='RandomSeed', value=69),
    player,
    dimensiondata,
])

# Top File
level = NBTFile()
level.tags.append(data)

level.write_file("level.dat")

# End portal tile entity
endportal = TAG_Compound()
endportal.tags.extend([
    TAG_String(name='id', value='end_portal'),
    TAG_Int(name='x', value=0),
    TAG_Int(name='y', value=63),
    TAG_Int(name='z', value=0),
    TAG_Byte(name='keepPacked', value=0),
])

# All tile entities — just one
tileentities = TAG_List(name='TileEntities', type=TAG_Compound)
tileentities.append(endportal)

# Block palette of the section
palette = TAG_List(name='Palette', type=TAG_Compound)
for value in ['minecraft:air', 'minecraft:end_stone', 'minecraft:end_portal']:
    block = TAG_String(name='Name', value=value)
    compound = TAG_Compound()
    compound.tags.append(block)
    palette.append(compound)

# Block states — A lot of it is just purely aesthetical
blockstates = TAG_Long_Array(name='BlockStates')
value = [0] * 256
for i in range(192, 240):
    value[i] = int('0b0001000100010001000100010001000100010001000100010001000100010001', 2)
value[240] = 2
blockstates.value = value

# Section Y coordinate
third = TAG_Compound()
third.tags.extend([
    TAG_Byte(name='Y', value=3),
    palette,
    blockstates,
])

# All sections — just one
sections = TAG_List(name='Sections', type=TAG_Compound)
sections.append(third)

# Chunk data — a lot of them is empty
level = TAG_Compound()
level.name = 'Level'
level.tags.extend([
    TAG_Int(name='xPos', value=0),
    TAG_Int(name='zPos', value=0),
    TAG_Byte(name='isLightOn', value=1),
    TAG_String(name='Status', value='full'),
    TAG_List(name='LiquidTicks', type=TAG_Compound),
    TAG_List(name='Entities', type=TAG_Compound),
    tileentities,
    sections,
])

# Top level, with the version value
chunk = NBTFile()
chunk.tags.extend([
    TAG_Int(name='DataVersion', value=1976),
    level,
])

# Writing region file
mkdir('DIM1')
mkdir('DIM1/region')
region = open('DIM1/region/r.0.0.mca', 'wb')
region.write(bytes(8192))
region = RegionFile('DIM1/region/r.0.0.mca')
region.write_chunk(0, 0, chunk)
