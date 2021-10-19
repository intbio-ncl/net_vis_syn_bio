
metadata = {'apiLevel': '2.1'}
def run(protocol):
    plate = protocol.load_labware('corning_96_wellplate_360ul_flat', 1)
    tiprack_1 = protocol.load_labware('opentrons_96_tiprack_300ul', 2)
    reservoir = protocol.load_labware('usascientific_12_reservoir_22ml', 4)
    p300 = protocol.load_instrument('p300_single', 'right', tip_racks=[tiprack_1])
    # distribute 20uL from reservoir:A1 -> plate:row:1
    # distribute 20uL from reservoir:A2 -> plate:row:2
    # etc...

    for i in range(8):
        p300.distribute(200, reservoir.wells()[i], plate.rows()[i])

    '''
    print(protocol.loaded_instruments)
    print(protocol.loaded_labwares)
    print(protocol.loaded_modules)

    for d in dir(protocol):
        print(d,eval(f'protocol.{d}'))
    '''
    