import os
import datetime
import time
directory = os.getcwd()
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import glob
import os
from threading import Timer,Thread,Event

#starttime = datetime.datetime.strptime("07/12/2017 15:30", "%m/%d/%Y %H:%M")
#endtime = datetime.datetime.strptime("07/12/2017 20:30", "%m/%d/%Y %H:%M")
def savitzky_golay(y, window_size, order, deriv=0, rate=1):
    r"""Smooth (and optionally differentiate) data with a Savitzky-Golay filter.
    The Savitzky-Golay filter removes high frequency noise from data.
    It has the advantage of preserving the original shape and
    features of the signal better than other types of filtering
    approaches, such as moving averages techniques.
    Parameters
    ----------
    y : array_like, shape (N,)
        the values of the time history of the signal.
    window_size : int
        the length of the window. Must be an odd integer number.
    order : int
        the order of the polynomial used in the filtering.
        Must be less then `window_size` - 1.
    deriv: int
        the order of the derivative to compute (default = 0 means only smoothing)
    Returns
    -------
    ys : ndarray, shape (N)
        the smoothed signal (or it's n-th derivative).
    Notes
    -----
    The Savitzky-Golay is a type of low-pass filter, particularly
    suited for smoothing noisy data. The main idea behind this
    approach is to make for each point a least-square fit with a
    polynomial of high order over a odd-sized window centered at
    the point.
    Examples
    --------
    t = np.linspace(-4, 4, 500)
    y = np.exp( -t**2 ) + np.random.normal(0, 0.05, t.shape)
    ysg = savitzky_golay(y, window_size=31, order=4)
    import matplotlib.pyplot as plt
    plt.plot(t, y, label='Noisy signal')
    plt.plot(t, np.exp(-t**2), 'k', lw=1.5, label='Original signal')
    plt.plot(t, ysg, 'r', label='Filtered signal')
    plt.legend()
    plt.show()
    References
    ----------
    .. [1] A. Savitzky, M. J. E. Golay, Smoothing and Differentiation of
       Data by Simplified Least Squares Procedures. Analytical
       Chemistry, 1964, 36 (8), pp 1627-1639.
    .. [2] Numerical Recipes 3rd Edition: The Art of Scientific Computing
       W.H. Press, S.A. Teukolsky, W.T. Vetterling, B.P. Flannery
       Cambridge University Press ISBN-13: 9780521880688
    """
    import numpy as np
    from math import factorial
    
    try:
        window_size = np.abs(np.int(window_size))
        order = np.abs(np.int(order))
    except ValueError, msg:
        raise ValueError("window_size and order have to be of type int")
    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order+1)
    half_window = (window_size -1) // 2
    # precompute coefficients
    b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
    m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - np.abs( y[1:half_window+1][::-1] - y[0] )
    lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve( m[::-1], y, mode='valid')
    
def donothing():
    time.sleep(1)

def h2so4TimeSeries(starttime, endtime):
    starttime_big = starttime - datetime.timedelta(hours=1)
    endtime_big = endtime + datetime.timedelta(hours = 1)
    hso4List = []
    no3List = []
    timeList = []
    t = 0.05
    k = 2.32e-9
    for filename in os.listdir(directory):
        if 'H2SO4_' in filename:
            filetime = datetime.datetime.strptime(filename.replace("H2SO4_H_","").rstrip(".txt"), "%Y-%m-%d_%H-%M-%S")
            if filetime > starttime_big:
                if filetime < endtime_big:
                    with open (filename,'rb') as myFile:
                        print ("opening " + filename)
                        with open ("tempyh2so4.txt","w") as tempOutputFile:
                            for line in myFile:
                                #try:
                                fullLine = line.split()
                                #print float(fullLine[0])
                                try:
                                    timee = datetime.datetime.strptime(' '.join(fullLine[2:8]), "%Y %m %d %H %M %S")
                                    if timee > starttime:
                                        if timee < endtime:
                                            #print("writing " + str(timee))
                                            #tempOutputFile.write(line)
                                            #timeList.append(timee-datetime.timedelta(hours=6))
                                            timeList.append(timee)
                                            hso4List.append(int(line.split()[24]))
                                            no3List.append(int(line.split()[15]))
                                except:
                                    print('oops')
                else:
                    print ("passing over " + filename)
            else:
                print ("passing over " + filename)
    timeListnp = np.array(timeList)
    hso4Listnp = np.transpose(np.array(hso4List))
    no3Listnp = np.transpose(np.array(no3List))
    #print h2so4List
    #print no3List
    h2so4Listnp = hso4Listnp/(no3Listnp*t*k)
    h2so4ListnpHat = savitzky_golay(h2so4Listnp, 201, 2)
    with open('h2so4conc.txt','w') as f:
        for i in h2so4Listnp:
            f.write(str(i))
    print np.average(h2so4Listnp)
    fig = plt.figure(figsize=(15,6))
    ax = fig.add_subplot(2,1,1)
    ax.clear()

    try:
        h2so4plot = ax.plot(timeListnp, h2so4ListnpHat)

        #ax.set_yscale('log')

        myFmt = mdates.DateFormatter("%m/%d/%y") #Format date
        myFmt2 = mdates.DateFormatter("%H:%M:%S") #Format time
        ax.xaxis.set_major_formatter(myFmt2)
        ax.xaxis.set_major_locator(mdates.SecondLocator(interval=int(((max(timeList)-min(timeList)).total_seconds())/5))) #6 marks on x axis
        ax.xaxis.set_minor_formatter(myFmt)
        ax.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
        ax.xaxis.set_tick_params(which='minor', pad=15) #Keeps major/minor axis from overlapping
        ax.set_ylabel('[H2SO4] (cm^-3)')
        ax.set_xlabel('Time (UTC)')
        ax.set_ylim([100000, 40000000])
        #plt.figtext(.5,.2, "Current [H2SO4] = " + str(np.mean(np.ndarray.tolist(h2so4)[-10:-1])), horizontalalignment='center', fontsize='xx-large')
        plt.xlim(min(timeListnp), max(timeListnp))
        ax.set_title('H2SO4 ' + str(min(timeListnp)) + ' - ' + str(max(timeListnp)) + ' (UTC)')        
        plt.savefig('H2SO4' + time.strftime("%m%d%Y-%H%M") + '.png', bbox_inches='tight', pad_inches=0)     
        plt.show()
    except:
        print 'error plotting data'
