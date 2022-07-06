import argparse
import asyncio

import bleak

BLE_LED_CHARACTERISTIC = '0000ffe1-0000-1000-8000-00805f9b34fb'

# For my LEDs, ff6633 is a vague, slightly embarrassing approximation of "warm white".

def _get_rgb_bytes(colour_str):
    rgb_bytes = bytes.fromhex(colour_str)
    if len(rgb_bytes) != 3:
        print('RGB colour must be 3 bytes')
        return None

    return rgb_bytes

def _colour_cmd(r, g, b):
    return bytes([126, 7, 5, 3, r, g, b, 0, 239])

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--scan', action='store_true', default=False, help='Scan for devices')
    parser.add_argument('--device', help='Device to connect to')
    parser.add_argument('--rgb', help='RGB color to set as 6 hex digits, eg ff6633 or 55ee55')
    parser.add_argument('--on', action='store_true')
    parser.add_argument('--off', action='store_true')
    parser.add_argument('--brightness', type=int)
    parser.add_argument('--rgbinteractive', action='store_true', default=False, help='Continually ask for colours')
    args = parser.parse_args()

    if args.scan:
        devices = await bleak.discover(timeout=5)
        for d in devices:
            print(d.name, d.address)
        return

    if not args.device:
        print('Please specify a device')
        return

    if args.rgb:
        rgb_bytes = _get_rgb_bytes(args.rgb)
        if not rgb_bytes:
            return
    else:
        rgb_bytes = None

    if args.on:
        cmd = bytes([126, 4, 4, 1, 255, 255, 255, 0, 239])
    elif args.off:
        cmd = bytes([126, 4, 4, 0, 255, 255, 255, 0, 239])
    elif args.rgb:
        rgb_bytes = _get_rgb_bytes(args.rgb)
        if not rgb_bytes:
            return

        cmd = _colour_cmd(*rgb_bytes)
    elif args.brightness:
        brightness = min(max(args.brightness, 0), 100)
        cmd = bytes([126, 4, 1, brightness, 255, 255, 255, 0, 239])

    async with bleak.BleakClient(args.device, timeout=10) as client:
        if args.rgbinteractive:
            while True:
                colour_str = input('Colour >').strip()
                if not colour_str:
                    break

                rgb_bytes = _get_rgb_bytes(colour_str)
                if not rgb_bytes:
                    break

                cmd = _colour_cmd(*rgb_bytes)

                await client.write_gatt_char(BLE_LED_CHARACTERISTIC, cmd)
        else:
            assert cmd
            await client.write_gatt_char(BLE_LED_CHARACTERISTIC, cmd)

if __name__ == '__main__':
    asyncio.run(main())
