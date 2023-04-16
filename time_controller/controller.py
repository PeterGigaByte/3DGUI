import asyncio
import time


class TimeController:
    def __init__(self):
        self.start_time = time.perf_counter()
        self.paused_time = 0
        self.time_scale = 1
        self.paused = False

    def now(self):
        if self.paused:
            return self.paused_time
        return (time.perf_counter() - self.start_time) * self.time_scale + self.paused_time

    def pause(self):
        if not self.paused:
            self.paused_time = self.now()
            self.paused = True

    def resume(self):
        if self.paused:
            self.start_time = time.perf_counter()
            self.paused = False

    def change_speed(self, factor):
        current_time = self.now()
        self.time_scale *= factor
        self.paused_time = current_time - (time.perf_counter() - self.start_time) * self.time_scale

    async def send_packet(self, packet_info):
        start_time = packet_info['fb_tx']
        print(f'Sending packet {packet_info["fId"]} to destination at requested time {start_time}')
        while self.now() < start_time:
            await asyncio.sleep(0.1)
        current_time = self.now()

        steps = 4
        step_duration = (packet_info['lb_tx'] - packet_info['fb_tx']) / steps

        for step in range(1, steps + 1):
            print(f'Packet {packet_info["fId"]} sent at step {step} at current time {current_time}')
            await asyncio.sleep(step_duration)
            current_time = self.now()

        print(f'Packet {packet_info["fId"]} received at destination at current time {current_time}')

    async def update_timeline(self):
        while True:
            # Wait for user input
            command = await asyncio.get_running_loop().run_in_executor(None, input,
                                                                       'Enter a command (p to pause, r to resume, '
                                                                       's to stop, f to speed up, d to slow down): \n')

            if command == 'p':
                # Pause the timeline
                self.pause()
                print('Timeline paused')

            elif command == 'r':
                # Resume the timeline
                self.resume()
                print('Timeline resumed')

            elif command == 's':
                # Stop the timeline
                break

            elif command == 'f':
                # Increase the time scaling factor by a factor of 2
                self.change_speed(2)
                print(f'Time scale factor increased to {self.time_scale}')

            elif command == 'd':
                # Decrease the time scaling factor by a factor of 2
                self.change_speed(0.5)
                print(f'Time scale factor decreased to {self.time_scale}')

            else:
                # Invalid command
                print('Invalid command')

            await asyncio.sleep(0.1)


# example of usage
time_controller = TimeController()


async def main():
    # Start the timeline update coroutine
    timeline_task = asyncio.create_task(update_timeline())

    # Schedule the packet sending tasks
    send_packet_tasks = [asyncio.create_task(send_packet(packet)) for packet in packet_data]

    # Run the tasks concurrently
    await asyncio.gather(timeline_task, *send_packet_tasks)


asyncio.run(main())
