from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
import pandas as pd
from scipy.integrate import cumtrapz
from scipy.integrate import trapz
import numpy as np
import statistics
from tkinter import filedialog

top = Tk()
top.title("Muse Headband Tools")
top.pack_propagate(0)
top.wm_minsize(width=1440, height=500)
top.wm_maxsize(width=1440, height=500)

class filebox:
    def __init__(self):
        self.main=Entry()
    def pack_filebox(self):
        self.main.grid(row=1, column = 1)

class message_window:
    def __init__(self):
        self.main=ScrolledText(width = 55, height  = 40)

    def pack_window(self):
       self.main.pack(side=RIGHT,padx=3)
		
class start_button:
    def __init__(self):
        self.blank_var=IntVar()
        self.blank_button=Checkbutton(text="Remove blank frames from sample", variable=self.blank_var, onvalue=1, offvalue=0)        
        
        self.button=Button()
        self.button['text']="Start"
        self.button['command']=self.start_clean
        
        self.var=IntVar()
        self.checkbutton=Checkbutton(text="Velocity clean", variable=self.var, onvalue=1, offvalue=0)        
        
        self.debugvar=IntVar()
        self.debug_button=Checkbutton(text="Show debug messages", variable=self.debugvar, onvalue=1, offvalue=0) 
        
        self.names=["TimeStamp","Delta_TP9","Delta_AF7","Delta_AF8","Delta_TP10","Theta_TP9","Theta_AF7","Theta_AF8","Theta_TP10","Alpha_TP9","Alpha_AF7","Alpha_AF8","Alpha_TP10","Beta_TP9","Beta_AF7","Beta_AF8","Beta_TP10","Gamma_TP9","Gamma_AF7","Gamma_AF8","Gamma_TP10","RAW_TP9","RAW_AF7","RAW_AF8","RAW_TP10","AUX_RIGHT","Accelerometer_Y","Accelerometer_Z","Accelerometer_X","Gyro_X","Gyro_Y","Gyro_Z","HeadBandOn","HSI_TP9","HSI_AF7","HSI_AF8","HSI_TP10","Battery Elements"]
        self.readings_per_second=Entry()
        self.file_label=Label(text="File to open: ")
        self.resolution_label=Label(text="Resolution (frames/second): ")
        
        self.split_at_all_var=IntVar()
        self.split_at_all_button=Checkbutton(text="Split by Big Break, Ravdess, and Control conditions", variable = self.split_at_all_var, onvalue = 1, offvalue = 0,pady = 15)
        self.split_at_all_button.grid(row = 5, column = 1, columnspan = 2)
        self.pack_first_split_buttons()
        self.pack_first_split_labels()
        
        self.split_happy_sad_var=IntVar()
        self.split_happy_sad_button=Checkbutton(text="Split Big Break and Ravdess conditions by happy/sad conditions",variable = self.split_happy_sad_var, onvalue = 1, offvalue = 0,pady = 20)
        self.split_happy_sad_button.grid(row = 9, column = 1, columnspan = 2)
        self.pack_internal_split_buttons()
        self.pack_internal_split_labels()
        
        self.bar=ttk.Progressbar(orient="horizontal",mode="indeterminate")

    def pack_start_button(self):
        self.button.grid(row = 2, column = 3)

    def pack_debug_button(self):
        self.debug_button.grid(row=0,column = 3)

    def pack_clean_and_threshold_button(self):
        self.checkbutton.grid(row=1, column = 3)

    def print_message(self,message): #Prints messages to the user console window
        message_window_.main.insert(INSERT, message + '\n')

    def pack_first_split_buttons(self):
        self.big_break_begining = Entry()
        self.big_break_end = Entry()
        self.big_break_begining.grid(row = 6, column = 1)
        self.big_break_end.grid(row = 6, column = 3)
        
        self.r_begining = Entry()
        self.r_end = Entry()
        self.r_begining.grid(row = 7, column = 1)
        self.r_end.grid(row = 7, column = 3)        
        
        self.control_begining = Entry()
        self.control_end = Entry()
        self.control_begining.grid(row = 8, column = 1)
        self.control_end.grid(row = 8, column = 3)
    
    def pack_first_split_labels(self):
    	self.bbb_label = Label(text="  Big Break condition begining time: ")
    	self.bbe_label = Label(text="  Big Break condition end time: ")
    	self.bbb_label.grid(row = 6, column = 0)
    	self.bbe_label.grid(row = 6, column = 2)
    	
    	self.rb_label = Label(text=" Ravdess condition begining time: ")
    	self.re_label = Label(text=" Ravdess condition end time: ")
    	self.rb_label.grid(row = 7, column = 0)
    	self.re_label.grid(row = 7, column = 2)
    	
    	self.control_b_label = Label(text="Control condition begining time: ")
    	self.control_e_label = Label(text="Control condition end time: ")
    	self.control_b_label.grid(row = 8, column = 0)
    	self.control_e_label.grid(row = 8, column = 2)
	
    def pack_internal_split_buttons(self):
        self.bb_happy_begin = Entry()
        self.bb_happy_end = Entry()
        self.bb_sad_begin = Entry()
        self.bb_sad_end = Entry()
        self.bb_happy_begin.grid(row = 10, column = 1)
        self.bb_happy_end.grid(row = 11, column = 1)
        self.bb_sad_begin.grid(row = 10, column = 3)
        self.bb_sad_end.grid(row = 11, column = 3)
		
        self.ravdess_happy_begin= Entry()
        self.ravdess_happy_end = Entry()
        self.ravdess_sad_begin = Entry()
        self.ravdess_sad_end = Entry()
        self.ravdess_happy_begin.grid(row = 12, column = 1)
        self.ravdess_sad_begin.grid(row = 12, column = 3)
        self.ravdess_happy_end.grid(row = 13, column = 1)
        self.ravdess_sad_end.grid(row = 13, column = 3)
		
    def pack_internal_split_labels(self):
        self.bb_happy_begin_label = Label(text = " Big Break, happy condition begining time: ")
        self.bb_happy_end_label = Label(text = " Big Break, happy condition end time: ")
        self.bb_sad_begin_label= Label(text = " Big Break, sad condition begining time: ")
        self.bb_sad_end_label= Label(text = " Big Break, sad condition end time: ")
        self.bb_happy_begin_label.grid(row = 10, column = 0)
        self.bb_sad_begin_label.grid(row=10, column = 2)
        self.bb_happy_end_label.grid(row = 11, column = 0)
        self.bb_sad_end_label.grid(row=11, column = 2)
        
        self.r_happy_begin_label = Label(text = "Ravdess, happy condition begining time: ")
        self.r_happy_end_label = Label(text = "Ravdess, happy condition end time: ")
        self.r_sad_begin_label = Label(text = "Ravdess, sad condition begining time: ")
        self.r_sad_end_label= Label(text = " Ravdess, sad condition end time: ")
        self.r_happy_begin_label.grid(row = 12, column = 0)
        self.r_sad_begin_label.grid(row = 12, column = 2)
        self.r_happy_end_label.grid(row = 13, column = 0)
        self.r_sad_end_label.grid(row = 13, column = 2)
        
    def is_pressed(self):
        if self.split_at_all_var ==1: return True
        return False
    
    def simple_time_calc(self, timeString):
    	colon_pointer = timeString.index(":")
    	minuteString = timeString[0:colon_pointer]
    	secondString = timeString[colon_pointer + 1:]
    	minutes = int(minuteString)
    	seconds = int(secondString) + minutes * 60
    	return seconds
    
    def export_depth1(self):
        file = open_file_box.main.get()
        self.big_break_df.to_csv(file[0:file.index('.')] + " Big_Break_df.csv")
        self.ravdess_df.to_csv(file[0:file.index('.')] + " Ravdess_df.csv")
        self.control_df.to_csv(file[0:file.index('.')] + " Control.csv")

    def timeHashGen(self):
        maxvalue = len(self.df.index)
        timeHash = {}
        initial_time = self.parse_time(self.df.iloc[0])
        counter=1
        while counter < maxvalue:
            int_seconds_time = self.parse_time(self.df.iloc[counter])
            elapsed_time = int_seconds_time - initial_time
            matching_timestamp = self.df.iloc[counter]["TimeStamp"]
            timeHash[int(elapsed_time)] = matching_timestamp
            counter += 1
        return timeHash
	
    def just_split_conditions_depth1(self):
        file = open_file_box.main.get()
        first_split = False
        to_skip = int(self.readings_per_second.get())
        try:
            self.df=pd.read_csv(file, low_memory=False)
            #Set up basic intervals using elapsed timestamps
            big_break_interval = [self.big_break_begining.get(), self.big_break_end.get()]
            ravdess_interval = [self.r_begining.get(), self.r_end.get()]   
            control_interval = [self.control_begining.get(), self.control_end.get()]
        	
        	#Convert the time format in those intervals to elapsed time
            big_break_interval[0] = self.simple_time_calc(big_break_interval[0])
            big_break_interval[1] = self.simple_time_calc(big_break_interval[1])
            ravdess_interval[0] = self.simple_time_calc(ravdess_interval[0])
            ravdess_interval[1] = self.simple_time_calc(ravdess_interval[1])
            control_interval[0] = self.simple_time_calc(control_interval[0])
            control_interval[1] = self.simple_time_calc(control_interval[1])
            
            #Multiply the timestamp of each condition by the number of recordings per second. Use this as a cutting template. Can't do this after cleaning
            self.big_break_df = self.df.iloc[big_break_interval[0]*to_skip:big_break_interval[1]*to_skip]
            self.ravdess_df = self.df.iloc[ravdess_interval[0]*to_skip:ravdess_interval[1]*to_skip]
            self.control_df = self.df.iloc[control_interval[0]*to_skip:control_interval[1]*to_skip]
                      
        except FileNotFoundError:
            message_window_.main.insert(INSERT, "File '" + file + "' not found \n")
    
    def just_split_conditions_depth2(self):
    	file = open_file_box.main.get()
    	to_skip = int(self.readings_per_second.get())
    	try:
    	    self.df=pd.read_csv(file, low_memory=False)
    	    
    	    #The control interval is unchanged, so let's deal with it now.
    	    control_interval = [self.control_begining.get(), self.control_end.get()]
    	    control_interval[0] = self.simple_time_calc(control_interval[0])
    	    control_interval[1] = self.simple_time_calc(control_interval[1])
    	    self.control_df = self.df.iloc[control_interval[0]*to_skip:control_interval[1]*to_skip]
            
    	#Pull the starting time stamps from the labels
    	    big_break_happy_start_timestamp = self.bb_happy_begin.get()
    	    big_break_sad_start_timestamp = self.bb_sad_begin.get()
    	    ravdess_happy_start_timestamp = self.ravdess_happy_begin.get()
    	    ravdess_sad_start_timestamp = self.ravdess_sad_begin.get()
    	
    	#Convert those starting times from time stamps to elapsed time
    	    big_break_happy_start_elapsed = self.simple_time_calc(big_break_happy_start_timestamp)
    	    big_break_sad_start_elapsed = self.simple_time_calc(big_break_sad_start_timestamp)
    	    ravdess_happy_start_elapsed = self.simple_time_calc(ravdess_happy_start_timestamp)
    	    ravdess_sad_start_elapsed = self.simple_time_calc(ravdess_sad_start_timestamp)
    	
    	#Generate dataframes for Big Break conditions
    	    if big_break_happy_start_elapsed > big_break_sad_start_elapsed:
    	        self.big_break_happy_df = self.df.iloc[big_break_happy_start_elapsed*to_skip : ]
    	        self.big_break_sad_df = self.df.iloc[0: big_break_happy_start_elapsed*to_skip]
                
    	    else:
    	        self.big_break_sad_df = self.df.iloc[big_break_sad_start_elapsed*to_skip : ]
    	        self.big_break_happy_df = self.df.iloc[0 : big_break_happy_start_elapsed *to_skip]
		
		#Generate dataframes for Ravdess conditions
    	    if ravdess_happy_start_elapsed > ravdess_sad_start_elapsed:
    	        self.ravdess_happy_df = self.df.iloc[ravdess_happy_start_elapsed*to_skip : ]
    	        self.ravdess_sad_df = self.df.iloc[0: ravdess_happy_start_elapsed*to_skip]
    	    else:
    	    	self.ravdess_sad_df = self.df.iloc[big_break_sad_start_elapsed* to_skip : ]
    	    	self.ravdess_happy_df = self.df.iloc[0 : ravdess_happy_start_elapsed* to_skip]
    	
    	except FileNotFoundError:
    	    message_window_.main.insert(INSERT, "File '" + file + "' not found \n")


    def export_depth2(self):
        file = open_file_box.main.get()
        self.control_df.to_csv(file[0:file.index('.')] + " Control.csv")
        self.big_break_happy_df.to_csv(file[0:file.index('.')] + " Big Break Happy.csv")
        self.big_break_sad_df.to_csv(file[0:file.index('.')] + " Big Break Sad.csv")
        self.ravdess_happy_df.to_csv(file[0:file.index('.')] + " Ravdess Happy.csv")
        self.ravdess_sad_df.to_csv(file[0:file.index('.')] + " Ravdess Sad.csv")
    
    def export_full_df(self):
        file = open_file_box.main.get()
        self.df_full.to_csv(file[0:file.index('.')] + "_velocity_cleaned.csv")
        
    def postCleanSplit_depth1(self):
        df = self.df_full
        #Set up basic intervals using elapsed timestamps
        big_break_interval = [self.big_break_begining.get(), self.big_break_end.get()]
        ravdess_interval = [self.r_begining.get(), self.r_end.get()]   
        control_interval = [self.control_begining.get(), self.control_end.get()]
        	
        #Convert the time format in those intervals to elapsed time
        big_break_interval[0] = self.simple_time_calc(big_break_interval[0])
        big_break_interval[1] = self.simple_time_calc(big_break_interval[1])
        ravdess_interval[0] = self.simple_time_calc(ravdess_interval[0])
        ravdess_interval[1] = self.simple_time_calc(ravdess_interval[1])
        control_interval[0] = self.simple_time_calc(control_interval[0])
        control_interval[1] = self.simple_time_calc(control_interval[1])
        
        # Since the indices are no longer directly related to time, a new system must be used. Convert the intervals to TimeStamps as they appear in the recording csv file.
        times = self.timeHashGen()
        big_break_interval[0] = times[big_break_interval[0]]
        big_break_interval[1] = times[big_break_interval[1]]
        ravdess_interval[0] = times[ravdess_interval[0]]
        ravdess_interval[1] = times[ravdess_interval[1]]
        control_interval[0] = times[control_interval[0]]
        control_interval[1] = times[control_interval[1]]
        
        #Convert the timestamps to the first index each time stamp occurs at in the recording csv file
        big_break_interval = [df.loc[df['TimeStamp']==big_break_interval[0]].index[0], df.loc[df['TimeStamp']==big_break_interval[1]].index[0]]
        ravdess_interval = [df.loc[df['TimeStamp']==ravdess_interval[0]].index[0], df.loc[df['TimeStamp']==ravdess_interval[1]].index[0]]
        control_interval = [df.loc[df['TimeStamp']==control_interval[0]].index[0], df.loc[df['TimeStamp']==control_interval[1]].index[0]]
		
		#Index between these timestamps to select the right row.
        self.big_break_df = df.iloc[big_break_interval[0]: big_break_interval[1]]
        self.ravdess_df = df.iloc[ravdess_interval[0]: ravdess_interval[1]]
        self.control_df = df.iloc[control_interval[0]: control_interval[1]]
         
    def postCleanSplit_depth2(self):
        
        df = self.df_full
                    
    	#Pull the starting time stamps from the labels
        big_break_happy_interval = [self.bb_happy_begin.get(), self.bb_happy_end.get()]
        big_break_sad_interval = [self.bb_sad_begin.get(), self.bb_sad_end.get()]
        ravdess_happy_interval = [ self.ravdess_happy_begin.get(), self.ravdess_happy_end.get() ]
        ravdess_sad_interval = [ self.ravdess_sad_begin.get(), self.ravdess_sad_end.get() ]
        control_interval = [self.control_begining.get(), self.control_end.get()]
    	
    	#Convert Big Break starting times from time stamps to elapsed time in seconds
        big_break_happy_interval[0] = self.simple_time_calc(big_break_happy_interval[0])
        big_break_happy_interval[1] = self.simple_time_calc(big_break_happy_interval[1])
        big_break_sad_interval[0] = self.simple_time_calc(big_break_sad_interval[0])
        big_break_sad_interval[1] = self.simple_time_calc(big_break_sad_interval[1])
        
        #Convert Ravdess starting times from time stamps to elapsed time in seconds
        ravdess_happy_interval[0] = self.simple_time_calc(ravdess_happy_interval[0])
        ravdess_happy_interval[1] = self.simple_time_calc(ravdess_happy_interval[1])
        ravdess_sad_interval[0] = self.simple_time_calc(ravdess_sad_interval[0])
        ravdess_sad_interval[1] = self.simple_time_calc(ravdess_sad_interval[1])
        
        #Convert control starting times from time stamps to elapsed time in seconds
        control_interval[0] = self.simple_time_calc(control_interval[0])
        control_interval[1] = self.simple_time_calc(control_interval[1])
        
        #Indices are no longer directly related to seconds after cleaning. We'll turn the times into a hashtable and lookup TimeStamps based on elapsed seconds.
        times = self.timeHashGen()
        
        #Convert Big Break elapsed time to TimeStamps
        big_break_happy_interval[0] = times[big_break_happy_interval[0]]
        big_break_happy_interval[1] = times[big_break_happy_interval[1]]
        big_break_sad_interval[0] = times[big_break_sad_interval[0]]
        big_break_sad_interval[1] = times[big_break_sad_interval[1]]
        
        #Convert Ravdess elapsed time to TimeStamps
        ravdess_happy_interval[0] = times[ravdess_happy_interval[0]]
        ravdess_happy_interval[1] = times[ravdess_happy_interval[1]]
        ravdess_sad_interval[0] = times[ravdess_sad_interval[0]]
        ravdess_sad_interval[1] = times[ravdess_sad_interval[1]]

		#Convert control elapsed time to TimeStamps
        control_interval[0] = times[ control_interval[0] ]
        control_interval[1] = times[ control_interval[1] ]
		
        #Convert the timestamps to the first index each time stamp occurs at in the recording csv file
        big_break_happy_interval = [df.loc[df['TimeStamp']==big_break_happy_interval[0]].index[0], df.loc[df['TimeStamp']==big_break_happy_interval[1]].index[0]]
        big_break_sad_interval = [df.loc[df['TimeStamp']==big_break_sad_interval[0]].index[0], df.loc[df['TimeStamp']==big_break_sad_interval[1]].index[0]]
        ravdess_happy_interval = [df.loc[df['TimeStamp']==ravdess_happy_interval[0]].index[0], df.loc[df['TimeStamp']==ravdess_happy_interval[1]].index[0]]
        ravdess_sad_interval = [df.loc[df['TimeStamp']==ravdess_sad_interval[0]].index[0], df.loc[df['TimeStamp']==ravdess_sad_interval[1]].index[0]]
        control_interval = [df.loc[df['TimeStamp']==control_interval[0]].index[0], df.loc[df['TimeStamp']==control_interval[1]].index[0]]

		#Create our dataframes. Index between these timestamps to select the right row.
        self.big_break_happy_df = df.iloc[big_break_happy_interval[0]: big_break_happy_interval[1]]
        self.big_break_sad_df = df.iloc[big_break_sad_interval[0]: big_break_sad_interval[1]]
        self.ravdess_happy_df = df.iloc[ravdess_happy_interval[0]: ravdess_happy_interval[1]]
        self.ravdess_sad_df = df.iloc[ravdess_sad_interval[0]: ravdess_sad_interval[1]]
        self.control_df = df.iloc[control_interval[0] : control_interval[1] ]

    def start_clean(self): #Starts a command to a cleaning application
        self.print_message("Welcome to MuseClean. Please be patient, as the duration of following process will depend on your processor and memory specifications \n")
        
        #Different paths are taken depending on the user's selection
        
        if self.var.get()==1 and self.split_at_all_var.get()==0 and self.split_happy_sad_var.get() == 0: #Just clean for velocity - no splitting of conditions	
            self.main_clean(open_file_box.main)
            self.export_full_df()
            return 0
        	
        elif self.var.get() ==0 and self.split_at_all_var.get()==1 and self.split_happy_sad_var.get() == 0: #Just split conditions with depth 1 - no cleaning for velocity
            self.just_split_conditions_depth1() #Create separate dataframes
            self.export_depth1() #Export those dataframes
            return 0
        
        elif self.var.get() == 0 and self.split_happy_sad_var.get() == 1: #Just split conditions with depth 2 - no cleaning for velocity)
            self.just_split_conditions_depth2() #Create separate dataframes
            self.export_depth2() #Export those dataframes
            return 0
        
        elif self.var.get() ==1 and self.split_at_all_var.get() == 1 and self.split_happy_sad_var.get() == 0: #Clean for velocity and then split for conditions with depth 1
            self.main_clean(open_file_box.main) #Clean
            self.postCleanSplit_depth1() #Split
            self.export_depth1() #Export
            return 0
        
        elif self.var.get() ==1 and self.split_happy_sad_var.get() == 1: #Clean for velocity and then split for conditions with depth 2
            self.main_clean(open_file_box.main) #Clean
            self.postCleanSplit_depth2() #Split
            self.export_depth2() #Export
            return 0
            
    def magnitude_acceleration(self,tupled_info):
        timestamp,accel_x,accel_y,accel_z=tupled_info[0],tupled_info[1],tupled_info[2],tupled_info[3]
        return (magnitude,timestamp)
    
    def parse_time(self,row):
        timestamp = row["TimeStamp"]
        mins=timestamp[timestamp.index(':')-2] +timestamp[timestamp.index(':')-1]
        seconds=timestamp[timestamp.index(':')+1] +timestamp[timestamp.index(':')+2]
        mils=timestamp[timestamp.index(':') + 4]
        final=(int(mins)*60+int(seconds)) + int(mils)/10 
        return final
    
    def mag_time_calc(self,counter,initial_time,df):
        row=self.df.iloc[counter]
        time=self.parse_time(row) - initial_time
        accel_x = float(row["Accelerometer_X"])*9.80665 #Convert from g's to m/s^2, as the muse headband tracks in m/s^2
        accel_y = float(row["Accelerometer_Y"])*9.80665
        accel_z = ((float(row["Accelerometer_Z"]))-.980665)*9.80665 #As the headband is relatively unmoved during the Muse session, we can just subtract gravity out, accepting a slight inaccuracy in our predictions
        magnitude=((accel_x**2) + (accel_y**2) + (accel_z**2))**(1/2)
        return [row["TimeStamp"],time,magnitude]		
	    
    def main_clean(self,entry):
        file=entry.get()
        first_split = False
        try:
            if self.var.get() ==0:
                print('Nothing to do here...')
                return None
            
            if self.is_pressed(): first_split = True
            self.df_full=pd.read_csv(file, low_memory=False)
            maxvalue = len(self.df_full.index)
            to_skip = int(self.readings_per_second.get())
            
            magnitudes=[]
            timestamps=[]
            timestamps_1d=[]
            
            selection=[]
            for i in range(0,maxvalue,to_skip):
            	selection.append(i)
            self.df=self.df_full.ix[selection] #Only deal with the rows we will integrate
            
            initial_time=self.parse_time(self.df.iloc[0])
            counter=1
            while counter < maxvalue//to_skip:
                our_info = self.mag_time_calc(counter,initial_time,self.df)
                temp=[our_info[0],our_info[1]]
                timestamps.append(temp)
                timestamps_1d.append(our_info[1])
                magnitudes.append(our_info[2])
                counter += 1
                
        #To calculate speed per second between time i-1 and time i, we subtract the i-1th integral (Using the fundamental theorem of calculus, integra from a to b is equal to integral of 0-->b minus integral of 0-->a) 

            raw_velocities=(cumtrapz(magnitudes[0:len(magnitudes)],x=timestamps_1d[0:len(magnitudes)]))
            velocities=[]
            i=0
            discarded=0
            max_value_velocity= len(raw_velocities)
            while i < max_value_velocity:
                velocity=(raw_velocities[i] - raw_velocities[i-1])
                if velocity >= 3:
                	self.df_full=self.df_full[self.df_full.TimeStamp != timestamps[i][0]]
                	discarded += 1
                i = i + 1
                
            forbidden_timestamps=[]
            if self.blank_var == 1: self.df_full.dropna()

            if self.debugvar.get()==1: self.print_message("Dropped " + str(discarded) + " seconds, out of a total of " + str(maxvalue//to_skip) + " seconds")
            
        except FileNotFoundError:
            message_window_.main.insert(INSERT, "File '" + file + "' not found \n")

Label(text="Written by Zachary Levine,\n this script is a set \n of tools for Muse Headbands.").grid(row=0,column=0)


start_button_btn=start_button()
start_button_btn.file_label.grid(row = 1, column = 0) #On the leftmost side, pack the "file to open" label
start_button_btn.blank_button.grid(row=3, column=0)

open_file_box=filebox() #Where to enter the CSV file to open
open_file_box.pack_filebox() #Next to the "file to open" label, pack the file entry box

start_button_btn.resolution_label.grid(row=2, column = 0) #Next to the filebox, pack the "resolution" label
start_button_btn.readings_per_second.grid(row=2, column = 1) #Next to the resolution label, pack the resolution entry box
start_button_btn.pack_start_button() #Pack the "start clean" button buttons
start_button_btn.pack_clean_and_threshold_button()  #Pack the button that gives the option to clean for speed
start_button_btn.pack_debug_button() #Option to show debug messages

message_window_=message_window() #Console message box
message_window_.pack_window()

mainloop() #Let the show begin