from inputs import get_gamepad
from parts.pwm import PCA9685


class Logitech_F710():
    name = "Gamepad"
    def __init__(self):

        self.events = None
        self.speed = 0
        self.angle = 0
        self.record = False
        self.stop_all = False
        self.save = False
        self.on = True

        print('Controller loading')

    def run_threaded(self):
        return self.speed, self.angle, self.record, self.stop_all, self.save

    def update(self):
        self.running=True
        while self.running:
            self.events = get_gamepad()

            for event in self.events:
                #print(event.ev_type, event.code, event.state)
                if event.ev_type == 'Absolute':
                    
                    if event.code == 'ABS_Y':
                        val = event.state
                        if val == 128 or -386 or 385:
                            self.speed = float(0)
                        if val > 385:
                            self.speed = float(val / 32767)
                        if val < -386:
                            self.speed = float(val / 32768)
                        print(self.speed)


                    elif event.code == 'ABS_RX':
                        if event.state == 128 or -386 or 385:
                            self.angle = float(0)
                        if event.state > 385:
                            self.angle = float(event.state / 32767)
                        if event.state < -386:
                            self.angle = float(event.state / 32768)
                        print(self.angle)



                if event.ev_type == 'Key':  

                    if event.code == 'BTN_SELECT':
                        if event.state == 1:
                            self.save = True
                            print('Save')
                            

                        if event.state == 0:
                            self.save = False
                            print('Save')    
                            
                    if event.code == 'BTN_START':
                        if event.state == 1:
                            self.stop_all = True
                            print('Stop All')

                    if event.code == 'BTN_TR':
                        if event.state == 1:
                            self.record = True
                            print('Record ON')

                    if event.code == 'BTN_TL':
                        if event.state == 1:
                            self.record = False 
                            print('Record OFF')         

            if not self.on:
                break

    def shutdown(self):
        self.on = False
        print('stoping Gamepad')
        time.sleep(.5)


class Xbox_F710():
    name = "Gamepad"

    def __init__(self):
        self.events = None
        self.speed = 0
        self.angle = 0
        self.record = False
        self.stop_all = False
        self.save = False
        self.assist = False
        self.on = True
        print('Controller loading')

    def run_threaded(self):
        return self.speed, self.angle, self.record, self.stop_all, self.save, self.assist

    def update(self):
        self.running = True
        while self.running:
            self.events = get_gamepad()

            for event in self.events:
                #print(event.ev_type, event.code, event.state)
                if event.ev_type == 'Absolute':

                    if event.code == 'ABS_Y':
                        if event.state == 127:
                            self.speed = float(0)
                        if event.state > 127:
                            self.speed = float((event.state - 127) / 128)
                        if event.state < 127:
                            self.speed = float((event.state - 127) / 127)
                        #print(self.speed)


                    elif event.code == 'ABS_Z':
                        if event.state == 128:
                            self.angle = float(0)
                        if event.state > 128:
                            self.angle = float((event.state - 128) / 127)
                        if event.state < 128:
                            self.angle = float((event.state - 128) / 128)
                        #print(self.angle)


                if event.ev_type == 'Key':

                    if event.code == 'BTN_TR2':
                        if event.state == 1:
                            self.save = True
                            print('Save')

                        if event.state == 0:
                            self.save = False
                            print('Save')

                    if event.code == 'BTN_TL2':
                        if event.state == 1:
                            self.stop_all = True
                            print('Stop All')

                    if event.code == 'BTN_Z':
                        if event.state == 1:
                            self.record = True
                            print('Record ON')

                    if event.code == 'BTN_WEST':
                        if event.state == 1:
                            self.record = False
                            print('Record OFF')

                    if event.code == 'BTN_SOUTH':
                        if event.state == 1:
                            self.assist = False
                            print('Assist OFF')

                    if event.code == 'BTN_NORTH':
                        if event.state == 1:
                            self.assist = True
                            print('Assist ON')

                    # if not self.on:
                    #    break

    def shutdown(self):
        self.on = False
        print('stoping Gamepad')
        time.sleep(.5)