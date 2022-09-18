
''' Demonstrates how to subscribe to and handle data from gaze and event streams '''
import math
import time
from turtle import end_fill
import csv

import adhawkapi
import adhawkapi.frontend
from adhawkapi import Events, MarkerSequenceMode, PacketType


class Frontend:
    ''' Frontend communicating with the backend '''
    BLINK_DATAPOINTS=30
    BLINK_TIME_ELAPSED=30

    FIX_DATAPOINTS=20
    FIX_TIME_ELAPSED=90

    #if trackloss exceeds a value over 5 times in 30s, unemployment
    TRACKLOSS_DATAPOINTS=10 #the amount of times youre allowed to go over max
    TRACKLOSS_TIME_ELAPSED=900
    TRACKLOSS_MAX= 5
    TRACKLOSS_SLEEP = 120

    trackloss_initial_time = 0
    trackloss_on = [False,False]
    trackloss_duration = 0
    eye_closed_time = 0
    eye_was_closed = False
    fixated_time = 0



    #analysis stuff
    total_blink_time = 0
    num_blinks =0
    dblink_sum =0
    data_point1=0
    data_point2=0
    prev_dblink_average=0
    dblink_average=0


    total_fixation_time =0
    num_fixation=0
    dfix_sum=0
    fdata_point1=0
    fdata_point2=0
    prev_dfix_average=0
    dfix_average=0
    sleep=False

    num_trackloss=0
    

    dblinklist = []
    dfixlist=[]

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
                # print(f'Blink duration in ms: + {args[0]}')
                Frontend.num_blinks+=1
                Frontend.total_blink_time+=args[0]
                #args[0] is duration in ms
                

            elif event_type == Events.SACCADE.value:
                Frontend.fixated_time = timestamp - Frontend.fixated_time - args[1]
                print(f'Fixated time: {Frontend.fixated_time}')

                if(Frontend.fixated_time>Frontend.TRACKLOSS_SLEEP):
                    Frontend.sleep=True
                else:
                    Frontend.total_fixation_time+=Frontend.fixated_time
                    Frontend.num_fixation+=1

                print(f'NUMBER OF FIXATIONS: {Frontend.num_fixation}')
                print(f'SUM OF FIXATIONS: {Frontend.total_fixation_time}')

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


            elif event_type == Events.TRACKLOSS_END.value:
                if Frontend.trackloss_on == [True,True]:
                    Frontend.trackloss_duration = timestamp - Frontend.trackloss_initial_time
                    # print(f'Trackloss Duration:{Frontend.trackloss_duration}')
                    Frontend.trackloss_on[args[0]] = False

                    if(Frontend.trackloss_duration>Frontend.TRACKLOSS_MAX):
                        Frontend.num_trackloss+=1
                        # print(f'TRACKLOSS RECORDED, num_trackloss is {Frontend.num_trackloss}')

                else:
                    Frontend.trackloss_on = [False,False]


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
    
    def create_baseline(self):
        total_seconds = 3600

        while total_seconds > 0:
            
            #blink duration
            #blink frequency
            #fixation duration
            #saccade peak velocity
            # eye closure time
            #pupil dilation range


            time.sleep(1)
            total_seconds-=1
        


    
    def get_baselines(self):
        with open("zone_data.csv", "r") as data:
            zone_data = csv.DictReader(data)

        #first row is header
        #first column is 

    def blink_analysis():

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

            if len(Frontend.dblinklist)==Frontend.BLINK_DATAPOINTS-1:
                Frontend.dblink_sum-=Frontend.dblinklist[0]
                Frontend.dblinklist.pop(0)
                Frontend.prev_dblink_average=Frontend.dblink_average
                Frontend.dblink_average=float(Frontend.dblink_sum/(Frontend.BLINK_DATAPOINTS-1))
        
        #start calculating derivative
        if Frontend.data_point1 !=0 and Frontend.data_point2 !=0:
            print(f'this is being appended to dblinklist {(Frontend.data_point2-Frontend.data_point1)/Frontend.BLINK_TIME_ELAPSED}')
            Frontend.dblinklist.append((Frontend.data_point2-Frontend.data_point1)/Frontend.BLINK_TIME_ELAPSED)
            Frontend.dblink_sum+=Frontend.dblinklist[len(Frontend.dblinklist)-1]


        print(f"Sum dblink is {Frontend.dblink_sum}")
        print(f"Average dblink is {Frontend.dblink_average}")
        print(f"previous average dblink is {Frontend.prev_dblink_average}")

        if(Frontend.dblink_average/Frontend.prev_dlink_average > 1.5):
            return False
        else:
            return True

        


    def fixation_analysis():

        #blink duration
        #fixation duration
        if Frontend.fdata_point1==0:
            Frontend.fdata_point1=(Frontend.total_fixation_time/Frontend.num_fixation)
            print(f'data point 1 is {Frontend.fdata_point1}')
        elif Frontend.fdata_point2==0:
            Frontend.fdata_point2=(Frontend.total_fixation_time/Frontend.num_fixation)
            print(f'data point 2 is {Frontend.fdata_point2}')
        else:
            Frontend.fdata_point1=Frontend.fdata_point2
            print(f'data point 1 is {Frontend.fdata_point1}')
            Frontend.fdata_point2=(Frontend.total_fixation_time/Frontend.num_fixation)
            print(f'data point 2 is {Frontend.fdata_point2}')

            if len(Frontend.dfixlist)==Frontend.FIX_DATAPOINTS-1:
                Frontend.dfix_sum-=Frontend.dfixlist[0]
                Frontend.dfixlist.pop(0)
                Frontend.prev_dfix_average=Frontend.dfix_average
                Frontend.dfix_average=float(Frontend.dfix_sum/(Frontend.FIX_DATAPOINTS-1))
        
        #start calculating derivative
        if Frontend.fdata_point1 !=0 and Frontend.fdata_point2 !=0:
            print(f'this is being appended to dfixlist {(Frontend.fdata_point2-Frontend.fdata_point1)/Frontend.FIX_TIME_ELAPSED}')
            Frontend.dfixlist.append((Frontend.fdata_point2-Frontend.fdata_point1)/Frontend.FIX_TIME_ELAPSED)
            print(f"Sum dfix is {Frontend.dfix_sum}")
            Frontend.dfix_sum += Frontend.dfixlist[len(Frontend.dfixlist)-1]
            


        print(f"Sum dfix is {Frontend.dfix_sum}")
        print(f"Average dfix is {Frontend.dfix_average}")
        print(f"previous average dfix is {Frontend.prev_dfix_average}")

        if(Frontend.dfix_average/Frontend.prev_dfix_average > 3):
            return False
        else:
            return True

def track_loss_analysis():
    
    return Frontend.num_trackloss<Frontend.TRACKLOSS_DATAPOINTS


        

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


        blink_counter =0
        fixation_counter=0
        trackloss_counter=0

        while True:
            blink_counter+=1
            fixation_counter+=1
            trackloss_counter+=1

            print(f'fixation count = {fixation_counter}')
            if(blink_counter>Frontend.BLINK_DATAPOINTS):
                #performs analysis HAVE ANALYSIS RETURNS A TRUE OR FALSE
                if(Frontend.num_blinks!=0 and Frontend.blink_analysis()==False):
                    print('NOT FIT TO WORK DUE TO BLINK')
                    frontend.shutdown()

                blink_counter=0
                Frontend.total_blink_time=0
                Frontend.num_blinks=0

            if(fixation_counter>Frontend.FIX_DATAPOINTS):
                if(Frontend.sleep==True):
                    frontend.shutdown()
                elif(Frontend.num_fixation!=0 and Frontend.fixation_analysis()==False):
                    print('NOT FIT TO WORK DUE TO FIXATION')
                    frontend.shutdown()
                fixation_counter=0
                Frontend.total_fixation_time=0
                Frontend.num_fixation=0

            if track_loss_analysis() == False:
                print('NOT FIT TO WORK DUE TO TRACKLOSS')
                frontend.shutdown()
            elif(trackloss_counter>Frontend.TRACKLOSS_TIME_ELAPSED):
                trackloss_counter=0
                
                Frontend.num_trackloss=0

            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):

        # Allows the frontend to be shut down robustly on a keyboard interrupt
        frontend.shutdown()


if __name__ == '__main__':
    main()
