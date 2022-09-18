
''' Demonstrates how to subscribe to and handle data from gaze and event streams '''

import time
from turtle import end_fill

import adhawkapi
import adhawkapi.frontend
from adhawkapi import Events, MarkerSequenceMode, PacketType


class Frontend:
    ''' Frontend communicating with the backend '''
    DATAPOINTS=5
    TIME_ELAPSED=10

    trackloss_initial_time = 0
    trackloss_on = [False,False]
    trackloss_eyes = [0,0]
    eye_closed_time = 0
    eye_was_closed = False
    duration = 0

    total_blink_time =0
    num_blinks =0
    dblink_sum =0
    data_point1=0
    data_point2=0
    prev_dblink_average=0

    blinklist =[]
    dblinklist = []

    def __init__(self):
        # Instantiate an API object
        self._api = adhawkapi.frontend.FrontendApi()

        # Tell the api that we wish to tap into the GAZE data stream
        # with self._handle_gaze_data_stream as the handler
        self._api.register_stream_handler(PacketType.GAZE, self._handle_gaze_data_stream)

        # Tell the api that we wish to tap into the EVENTS stream
        # with self._handle_event_stream as the handler
        self._api.register_stream_handler(PacketType.EVENTS, self._handle_event_stream)

        # Start the api and set its connection callback to self._handle_connect_response. When the api detects a
        # connection to a MindLink, this function will be run.
        self._api.start(connect_cb=self._handle_connect_response)

        self._api.register_stream_handler(PacketType.PUPIL_DIAMETER, self.handler_pupil_stream)
        

        # Disallows console output until a Quick Start has been run
        self._allow_output = False

        # Used to limit the rate at which data is displayed in the console
        self._last_console_print = None

        # Flags the frontend as not connected yet
        self.connected = False


        print('Starting frontend...')

    def shutdown(self):
        ''' Shuts down the backend connection '''

        # Stops api camera capture
        self._api.stop_camera_capture(lambda *_args: None)

        # Stop the log session
        self._api.stop_log_session(lambda *_args: None)

        # Shuts down the api
        self._api.shutdown()

    def quickstart(self):
        ''' Runs a Quick Start using AdHawk Backend's GUI '''

        # The MindLink's camera will need to be running to detect the marker that the Quick Start procedure will
        # display. This is why we need to call self._api.start_camera_capture() once the MindLink has connected.
        self._api.quick_start_gui(mode=MarkerSequenceMode.FIXED_GAZE, marker_size_mm=35,
                                  callback=(lambda *_args: None))

        # Allows console output
        self._allow_output = True

    def _handle_gaze_data_stream(self, timestamp, x_pos, y_pos, z_pos, vergence):
        ''' Prints gaze data to the console '''

        # Only log at most once per second
        if self._last_console_print and timestamp < self._last_console_print + 1:
            return


        # if self._allow_output:
        #     self._last_console_print = timestamp
        #     print(f'Gaze data\n'
        #           f'Time since connection:\t{timestamp}\n'
        #           f'X coordinate:\t\t{x_pos}\n'
        #           f'Y coordinate:\t\t{y_pos}\n'
        #           f'Z coordinate:\t\t{z_pos}\n'
        #           f'Vergence angle:\t\t{vergence}\n')


    def _handle_event_stream(self, event_type, timestamp, *args):
        ''' Prints event data to the console '''
        if self._allow_output:

            # We discriminate between events based on their type
            if event_type == Events.BLINK.value:
                blink_str = args[0]
                print(f'Blink duration in ms: + {blink_str}')
                Frontend.num_blinks+=1
                Frontend.total_blink_time+=args[0]
                print(f'total number of blinks {Frontend.num_blinks}')
                print(f'total time blinked {Frontend.total_blink_time}')
                

                #args[0] is duration in ms
                

            elif event_type == Events.SACCADE.value:
            #     print('Saccade!')
                pass
                # print(f'Saccade duration: {args[0]}')
                # print(f'Saccade amp: {args[1]}')

            # if event_type == Events.EYE_CLOSED.value:
            #     #print('Eye closed!')
            #     Frontend.eye_closed_time = timestamp
            #     Frontend.eye_was_closed = True

            # if event_type == Events.EYE_OPENED.value:
            #     #print('Eye opened!')
            #     if Frontend.eye_was_closed:
            #         duration = timestamp - Frontend.eye_closed_time
            #         #print(f'Eye was closed for: + {duration}')
            #         Frontend.eye_was_closed = False

            elif event_type == Events.TRACKLOSS_START.value:
                Frontend.trackloss_on[args[0]] = True

                if Frontend.trackloss_on == [True,True]:
                    Frontend.trackloss_initial_time = timestamp


            # if event_type == Events.TRACKLOSS_END.value:
            #     Frontend.trackloss_on[args[0]] = False
            
            # elif event_type == Events.TRACKLOSS_END.value:

            #     Frontend.trackloss_eyes[args[0]] = (timestamp - Frontend.trackloss_initial_time)
            #     Frontend.trackloss_initial_time[args[0]] = 0

            #     if 0 in Frontend.trackloss_eyes[args[0]]:
            #         Frontend.duration = Frontend.trackloss[args[0]] - Frontend.trackloss_initial_time
            #         Frontend.duration[args[0]] = 0
                
            #     else: 
            #         Frontend.duration = min(Frontend.trackloss_eyes[0]+ Frontend.trackloss_eyes[1]) - Frontend.trackloss_initial_time
            #         Frontend.duration = [0,0]

                
                # if args[0]==0:
                #     right_duration = timestamp - Frontend.trackloss_initial_time
                #     print(f'right trackloss duration was {right_duration}')
                # else:
                #     left_duration = timestamp - Frontend.trackloss_initial_time
                #     print(f'left trackloss duration was {left_duration}')
                
                # if Frontend.trackloss_on == [False,False]:
                #     Frontend.total_duration = (right_duration+left_duration)/2
                #     print(f'average trackloss duration was {Frontend.total_duration}')
                

            

    def handler_pupil_stream(self, timestamp, *data):
        right_pupil, left_pupil = data

        if self._last_console_print and timestamp < self._last_console_print + 1:
            return

        if self._allow_output:
            self._last_console_print = timestamp
            # print(f'right diametre: {data[0]}')
            # print(f'left diametre: {data[1]}')

        


    def _handle_connect_response(self, error):
        ''' Handler for backend connections '''

        # Starts the camera and sets the stream rate
        if not error:
            print('Connected to AdHawk Backend Service')

            # Sets the GAZE data stream rate to 125Hz
            self._api.set_stream_control(PacketType.GAZE, 125, callback=(lambda *_args: None))

            # Tells the api which event streams we want to tap into. In this case, we wish to tap into the BLINK and
            # SACCADE data streams.
            self._api.set_event_control(adhawkapi.EventControlBit.BLINK, 1, callback=(lambda *_args: None))
            self._api.set_event_control(adhawkapi.EventControlBit.SACCADE, 1, callback=(lambda *_args: None))
            self._api.set_event_control(adhawkapi.EventControlBit.EYE_CLOSE_OPEN, 1, callback=(lambda *_args: None))
            self._api.set_event_control(adhawkapi.EventControlBit.TRACKLOSS_START_END, 1, callback=(lambda *_args: None))
            self._api.set_stream_control(PacketType.PUPIL_DIAMETER, 1, callback=(lambda *_args: None) )
            # Starts the MindLink's camera so that a Quick Start can be performed. Note that we use a camera index of 0
            # here, but your camera index may be different, depending on your setup. On windows, it should be 0.
            self._api.start_camera_capture(camera_index=0, resolution_index=adhawkapi.CameraResolution.MEDIUM,
                                           correct_distortion=False, callback=(lambda *_args: None))
            # Starts a logging session which saves eye tracking signals. This can be very useful for troubleshooting
            self._api.start_log_session(log_mode=adhawkapi.LogMode.BASIC, callback=lambda *args: None)

            # Flags the frontend as connected
            self.connected = True

    def analysis():
        
        dblink_average=0

        if Frontend.data_point1==0:
            Frontend.data_point1=(Frontend.total_blink_time/Frontend.num_blinks)
            print(f'data point 1 is {Frontend.data_point1}')
        elif Frontend.data_point2==0:
            Frontend.data_point2=(Frontend.total_blink_time/Frontend.num_blinks)
            print(f'data point 2 is {Frontend.data_point2}')
        else:
            Frontend.data_point1=Frontend.data_point2
            print(f'data point 1 is {Frontend.data_point1}')
            Frontend.data_point2=(Frontend.total_blink_time/Frontend.num_blinks)
            print(f'data point 2 is {Frontend.data_point2}')

            if len(Frontend.dblinklist)==Frontend.DATAPOINTS-1:
                Frontend.dblink_sum-=Frontend.dblinklist[0]
                Frontend.dblinklist.pop(0)
                Frontend.prev_dblink_average=dblink_average
                dblink_average=float(Frontend.dblink_sum/(Frontend.DATAPOINTS-1))
        
        #start calculating derivative
        if Frontend.data_point1 !=0 and Frontend.data_point2 !=0:
            print(f'this is being appended to dblinklist {(Frontend.data_point2-Frontend.data_point1)/Frontend.TIME_ELAPSED}')
            Frontend.dblinklist.append((Frontend.data_point2-Frontend.data_point1)/Frontend.TIME_ELAPSED)
            Frontend.dblink_sum+=Frontend.dblinklist[len(Frontend.dblinklist)-1]


        print(f"Sum dblink is {Frontend.dblink_sum}")
        print(f"Average dblink is {dblink_average}")
        print(f"previous average dblink is {Frontend.prev_dblink_average}")

        



def main():
    '''Main function'''

    frontend = Frontend()
    try:
        print('Plug in your MindLink and ensure AdHawk Backend is running.')
        while not frontend.connected:
            pass  # Waits for the frontend to be connected before proceeding

        input('Press Enter to run a Quick Start.')

        # Runs a Quick Start at the user's command. This tunes the scan range and frequency to best suit the user's eye
        # and face shape, resulting in better tracking data. For the best quality results in your application, you
        # should also perform a calibration before using gaze data.
        frontend.quickstart()


        counter =0
        while True:
            counter+=1
            if(counter>Frontend.DATAPOINTS):
                #performs analysis
                if(Frontend.num_blinks!=0):
                    Frontend.analysis()

                counter=0
                Frontend.total_blink_time=0
                Frontend.num_blinks=0

            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):

        # Allows the frontend to be shut down robustly on a keyboard interrupt
        frontend.shutdown()


if __name__ == '__main__':
    main()
