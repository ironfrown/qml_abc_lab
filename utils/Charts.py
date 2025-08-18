# Support functions for TS plotting
# Author: Jacob Cybulski, ironfrown[at]gmail.com
# Aims: Provide support for quantum time series analysis
# Date: 2024

import os
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import set_loglevel
set_loglevel("error")

from IPython.display import clear_output

##### PL histograms

### Plot probability distribution
#   probs: list or tensor
#   thres: all probs less that threshold will not be plotted
def plot_curve(X, y, scale=None, rcParams=(8, 6), dpi=72, xlim=None, ylim=None, 
               col='blue', linestyle='solid', marker=None, mfc='white', rot=0,
               label=None, xlabel='Range', ylabel='Values', title='Data', save_plot=None):

    # Prepare data
    n_data = len(X)

    # Plot the results
    plt.rcParams["figure.figsize"] = rcParams   
    plt.rcParams["figure.dpi"] = dpi
    if xlim is not None: plt.xlim(xlim)
    if ylim is not None: plt.ylim(ylim)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(rotation=rot)
    if scale is not None:
        dpi = fig.get_dpi()
        fig.set_dpi(dpi*scale)
    plt.plot(X, y, color=col, linestyle=linestyle, marker=marker, mfc=mfc)
    if save_plot is not None:
        os.makedirs(os.path.dirname(save_plot), exist_ok=True)
        ext = os.path.splitext(save_plot)[1][1:]
        plt.savefig(save_plot, format=ext)
    plt.show()


### Plot probability distribution
#   probs: list or tensor
#   thres: all probs less that threshold will not be plotted
def plot_hist(probs, scale=None, figsize=(8, 6), dpi=72, th=-10000, xlim=None, ylim=None, bottom=0, 
              labels=None, xlabel='Results', ylabel='Probability', title='Measurement Outcomes'):

    # Prepare data
    n_probs = len(probs)
    n_digits = len(bin_int_to_list(n_probs, 1)) # 1 means as many digits as required
    if labels is None: labels = [f'{n:0{n_digits}b}' for n in np.arange(n_probs)]

    # Filter out the prob values below threshold
    pairs = [(p, l) for (p, l) in zip(probs, labels) if p >= th]
    probs = [p for (p, l) in pairs]
    labels = [l for (p, l) in pairs]

    # Plot the results
    fig, ax=plt.subplots(figsize=figsize, dpi=dpi)
    ax.bar(labels, probs)
    plt.axhline(y=0, color="lightgray", linestyle='-')
    ax.set_title(title)
    if xlim is not None: plt.xlim(xlim)
    if ylim is not None: plt.ylim(ylim)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=60)
    if scale is not None:
        dpi = fig.get_dpi()
        fig.set_dpi(dpi*scale)
    plt.show()


### Plot two probability distributions side-by-side
#   probs_1, probs_2: Two tensors of probabilities
#   thres: all probs less that threshold will not be plotted
def plot_compare_hist(probs_1, probs_2, scale=None, figsize=(8, 6), dpi=72, th=0, 
                      title_1='Measurement Outcomes 1', title_2='Measurement Outcomes 2',
                      xlabel_1='Results', xlabel_2='Results',
                      ylabel_1='Probability', ylabel_2='Probability'):

    # Prepare data
    n_probs_1 = len(probs_1)
    n_digits_1 = len(bin_int_to_list(n_probs_1, 1)) # 1 means as many digits as required
    labels_1 = [f'{n:0{n_digits_1}b}' for n in np.arange(n_probs_1)]
    n_probs_2 = len(probs_2)
    n_digits_2 = len(bin_int_to_list(n_probs_2, 1)) # 1 means as many digits as required
    labels_2 = [f'{n:0{n_digits_2}b}' for n in np.arange(n_probs_2)]

    # Filter out the prob values below threshold
    pairs_1 = [(p, l) for (p, l) in zip(probs_1, labels_1) if p >= th]
    probs_1 = [p for (p, l) in pairs_1]
    labels_1 = [l for (p, l) in pairs_1]
    pairs_2 = [(p, l) for (p, l) in zip(probs_2, labels_2) if p >= th]
    probs_2 = [p for (p, l) in pairs_2]
    labels_2 = [l for (p, l) in pairs_2]

    # Plot the results
    fig, axs = plt.subplots(1, 2, figsize=figsize, dpi=dpi)
    axs[0].bar(labels_1, probs_1)
    axs[0].set_title(title_1)
    axs[0].set_xlabel(xlabel_1)
    axs[0].set_ylabel(ylabel_1)
    axs[0].tick_params(labelrotation=60)
    axs[1].bar(labels_2, probs_2)
    axs[1].set_title(title_2)
    axs[1].set_xlabel(xlabel_2)
    axs[1].set_ylabel(ylabel_2)
    axs[1].tick_params(labelrotation=60)

    if scale is not None:
        dpi = fig.get_dpi()
        fig.set_dpi(dpi*scale)
    plt.show()

### Exponential Moving Target used to smooth the lines 
def smooth_movtarg(scalars, weight):  # Weight between 0 and 1
    last = scalars[0]  # First value in the plot (first timestep)
    smoothed = list()
    for point in scalars:
        smoothed_val = last * weight + (1 - weight) * point  # Calculate smoothed value
        smoothed.append(smoothed_val)                        # Save it
        last = smoothed_val                                  # Anchor the last smoothed value        
    return smoothed

### Plot performance measures
def meas_plot(meas_vals, rcParams=(8, 4), dpi=72, yscale='linear', log_interv=1, task='min',
                  backplot=False, back_color='linen', smooth_weight=0.9, save_plot=None,
                  meas='cost', title_pref='', xlim=None, ylim=None):
        
    if task == 'min':
        opt_cost = min(meas_vals)
        x_of_opt = np.argmin(meas_vals)
    else:
        opt_cost = max(meas_vals)
        x_of_opt = np.argmax(meas_vals)
    iter = len(meas_vals)
    smooth_fn = smooth_movtarg(meas_vals, smooth_weight)
    clear_output(wait=True)
    plt.rcParams["figure.figsize"] = rcParams   
    plt.rcParams["figure.dpi"] = dpi
    plt.title(f'{title_pref} {meas} vs iteration '+('with smoothing ' if smooth_weight>0 else ' '))
    plt.xlabel(f'Iteration (best {meas}={np.round(opt_cost, 4)} @ iter# {x_of_opt*log_interv})')
    plt.ylabel(f'{meas.title()}')
    if xlim is not None: plt.xlim(xlim)
    if ylim is not None: plt.ylim(ylim)
    plt.axvline(x=x_of_opt*log_interv, color="lightgray", linestyle='--')
    plt.yscale(yscale)
    if backplot:
        plt.plot([x*log_interv for x in range(len(meas_vals))], meas_vals, color=back_color) # lightgray
    plt.plot([x*log_interv for x in range(len(smooth_fn))], smooth_fn, color='black')
    if save_plot is not None:
        os.makedirs(os.path.dirname(save_plot), exist_ok=True)
        ext = os.path.splitext(save_plot)[1][1:]
        plt.savefig(save_plot, format=ext)
    plt.show()


### Plot a list of series, where each series may start at a differ X point
#   y_list: a list of series with equidistant points
#   X_list: a list of starting X points for each series
#   labels, color, lines, marks: Plot features for each series
#   other: standard plot properties
def multi_plot_flat_ts(
    y_list, X_list=None, labels=None, colors=None, lines=None, markers=None, marker_colors=None,
    xlim=None, ylim=None, rcParams=(12, 6), dpi=72, xlabel='Range', ylabel='Target value',
    legend_cols=3, title='Time series plot', save_plot=None):

    # labels=['Target function', 'Training data', 'Test data', 'Fitted model', 'Model predictions'],
    # colors=['lightblue', 'lightblue', 'pink', 'blue', 'red'],
    # linestyles=['dashed', 'solid', 'solid', 'dashed', 'dashed'],

    if len(y_list) == 0:
        print(f'*** Error: the list of data to plot cannot be empty')
        return
        
    # Missing main parameters
    if X_list is None or len(X_list) == 0:
        X_list = [0] # [[i for i in ]]
    if len(X_list) < len(y_list):
        ts_start = X_list[-1]+len(y_list[len(X_list)])
        for ts in y_list[len(X_list):]:
            X_list.append(ts_start)
            ts_start += len(ts)

    if labels is None or len(labels) == 0:
        labels = [f'Plot {0:02d}']
    if len(labels) < len(y_list):
        for i in range(len(labels), len(y_list)):
            labels.append(f'Plot {i:02d}')

    cmap = matplotlib.colormaps['Set1']
    map_colors = cmap.colors+cmap.colors+cmap.colors
    if colors is None or len(colors) == 0:
        colors = [map_colors[0]]
    if len(colors) < len(y_list):
        for i in range(len(colors), len(y_list)):
            colors.append(map_colors[i])

    if marker_colors is None or len(marker_colors) == 0:
        marker_colors = colors
    if len(marker_colors) < len(y_list):
        for i in range(len(marker_colors), len(y_list)):
            marker_colors.append(colors[i])

    if lines is None or len(lines) == 0:
        lines = ['solid']
    if len(lines) < len(y_list):
        lines = lines+['solid']*(len(y_list)-len(lines))
    
    if markers is None or len(markers) == 0:
        markers = ['none']
    if len(markers) < len(y_list):
        markers = markers+['none']*(len(y_list)-len(markers))
    
    # Parameter values
    plt.rcParams["figure.figsize"] = rcParams   
    plt.rcParams["figure.dpi"] = dpi

    if xlim is not None:
        plt.xlim(xlim[0], xlim[1])
    if ylim is not None:
        plt.ylim(ylim[0], ylim[1])

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # Calculate the X_range for each list
    
    for i in range(len(y_list)):
        xfirst = X_list[i]
        xlast = X_list[i]+len(y_list[i])
        xrange = range(xfirst, xlast)
        plt.plot(xrange, y_list[i], linestyle=lines[i], marker=markers[i], 
                 color=colors[i], mec=colors[i], mfc=marker_colors[i], label=labels[i])
        if i > 0:
            plt.axvline(x = X_list[i]-0.5, color = 'lightgray', linestyle='dashed')
    
    plt.legend(loc='best', ncol=legend_cols)
    
    if save_plot is not None:
        os.makedirs(os.path.dirname(save_plot), exist_ok=True)
        ext = os.path.splitext(save_plot)[1][1:]
        plt.savefig(save_plot, format=ext)
    plt.show()    

### Plot the target function and data
def plot_train_and_test_data(
    X_org, y_org, X_train, y_train, X_valid, y_valid,
    y_train_hat=None, y_valid_hat=None,
    xlim=None, ylim=None, rcParams=(12, 6), dpi=72,
    legend_cols=3, marker='o', markers=None,
    labels=['Target function', 'Training data', 'Test data', 'Fitted model', 'Model predictions'],
    colors=['lightblue', 'lightblue', 'pink', 'blue', 'red'],
    linestyles=['dashed', 'solid', 'solid', 'dashed', 'dashed'],
    xlabel='Range', ylabel='Target value',
    title='Target function with noisy data',
    save_plot=None):

    # Parameter values
    plt.rcParams["figure.figsize"] = rcParams
    plt.rcParams["figure.dpi"] = dpi
        
    if xlim is not None:
        plt.xlim(xlim[0], xlim[1])
    if ylim is not None:
        plt.ylim(ylim[0], ylim[1])
    if markers is None:
        markers = [marker, marker, marker, marker, marker]

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
    # Plot target function
    if linestyles[0] != 'none':
        plt.plot(X_org, y_org, color=colors[0], linestyle=linestyles[0], mfc='white', marker=markers[0], label=labels[0])
    plt.plot(X_train, y_train, color=colors[1], linestyle=linestyles[1], mfc='white', marker=markers[1], label=labels[1])
    plt.plot(X_valid, y_valid, color=colors[2], linestyle=linestyles[2], mfc='white', marker=markers[2], label=labels[2])

    # Plot fitted line
    if y_train_hat is not None:
        plt.plot(X_train, y_train_hat, color=colors[3], linestyle=linestyles[3], mfc='white', marker=markers[3], label=labels[3])
    
    # Plot prediction
    if y_valid_hat is not None:
        plt.plot(X_valid, y_valid_hat, color=colors[4], linestyle=linestyles[4], mfc='white', marker=markers[4], label=labels[4])

    plt.axvline(x = (X_train[-1]+X_valid[0])/2, color = 'lightgray', linestyle='dashed')
    plt.legend(loc='best', ncol=legend_cols)
    
    if save_plot is not None:
        os.makedirs(os.path.dirname(save_plot), exist_ok=True)
        ext = os.path.splitext(save_plot)[1][1:]
        plt.savefig(save_plot, format=ext)

    plt.show()    


### Plot and compare various performance plots
#   If log_interv is a number, it applies to all curves
#   If it is a list, each number applies to its curve
def multi_perform_plot(pvals, log_interv=1, rcParams=(8, 4), dpi=72, 
                  yscale='linear', smooth_weight=0.9, smooth_type='emt', save_plot=None,
                  title='Performance vs iteration', meas_type='Cost', ylabel='Cost', xlabel='Iteration',
                  meas_min=True, labels=[], line_styles=None, line_cols=None, prec=None,
                  backplot=False, back_color='linen', col_cycle_rep=10, opt_format=None,
                  legend_fsize=None, legend_cols=1, legend_lim=20, xlim=None, ylim=None):
    
    if not pvals: # Empty list of curves
        return
    if type(log_interv) is int:
        log_int_list = [log_interv]*len(pvals)
    elif type(log_interv) is list:
        log_int_list = log_interv
    else:
        print('*** log_interv must be an interger or a list')
        return

    plt.rcParams["figure.figsize"] = rcParams
    plt.rcParams["figure.dpi"] = dpi
    prop_cycle = plt.rcParams['axes.prop_cycle']
    default_cols = prop_cycle.by_key()['color']
    if line_cols is None: line_cols = default_cols*col_cycle_rep
    if line_styles is None: line_styles = ['solid']*len(pvals)
    if legend_fsize is None: legend_fsize = 'small'
    fig, ax = plt.subplots()

    iter = max([len(p) for p in pvals])*max(log_int_list)
    smooth_text = f'sm.{smooth_type}={smooth_weight:.2f}, ' if smooth_weight>0 else ''
    plt.title(f'{title} ({smooth_text}iter# {iter})')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if xlim is not None: plt.xlim(xlim)
    if ylim is not None: plt.ylim(ylim)
    plt.yscale(yscale)
    for i in range(len(pvals)):
        if backplot:
            plt.plot([x*log_int_list[i] for x in range(len(pvals[i]))], pvals[i], color=back_color)
    for i in range(len(pvals)):
        if meas_min:
            lim = 'min'
            sel_val = min(pvals[i])
            sel_x = np.argmin(pvals[i])
        else:
            lim = 'max'
            sel_val = max(pvals[i])
            sel_x = np.argmax(pvals[i])
        smooth_vals = smooth_movtarg(pvals[i], smooth_weight)
        sel_lab = labels[i] if labels else f'{i}'
        sel_val = np.round(sel_val, prec) if prec is not None else sel_val
        sel_val_text = f'{sel_val}' if opt_format is None else f'{sel_val:{opt_format}}'
        plt.plot([x*log_int_list[i] for x in range(len(pvals[i]))], smooth_vals, 
                 linestyle=line_styles[i], color=line_cols[i],
                 label=f'{sel_lab}  ({lim} {meas_type}={sel_val_text} @ iter# {sel_x*log_int_list[i]})')
    plt.legend(loc='best', ncol=legend_cols, fontsize=legend_fsize)
    if len(pvals) > legend_lim: ax.get_legend().remove()
    if save_plot is not None:
        os.makedirs(os.path.dirname(save_plot), exist_ok=True)
        ext = os.path.splitext(save_plot)[1][1:]
        plt.savefig(save_plot, format=ext)
    plt.show()


### Plot a list of objective function instances 
### Each objective function value could be of different length
def plot_objfn_range(objective_fn, smooth_weight=0, log_interv=1,
                     objfn_name='Model', objfn_list=None, meas_min=True,
                     title = 'Range of objective function values for all model instances',
                     xlabel = 'Iterations', ylabel = 'Objective Function Value', meas_type='mean cost',
                     color = ['red', 'blue', 'orange', 'green', 'black', 'black', 'black', 'black', 'black'], 
                     linestyles=['solid', 'solid', 'solid', 'solid', 'solid', 'solid', 'solid', 'solid', 'solid'],
                     xlim=None, ylim=None, rcParams=(8, 4), dpi=72, prec=None, opt_format=None, save_plot = None):

    ### Smooth the array of values
    def smooth(scalars, weight):  # Weight between 0 and 1
        last = scalars[0]  # First value in the plot (first timestep)
        smoothed = list()
        for point in scalars:
            smoothed_val = last * weight + (1 - weight) * point  # Calculate smoothed value
            smoothed.append(smoothed_val)                        # Save it
            last = smoothed_val                                  # Anchor the last smoothed value
            
        return smoothed

    ### Resize all arrays in a list to the longest
    ### Then pad them to their last value
    def resize_to_equal_and_pad(arrays):
        
        # Find the length of the longest array
        max_length = max(arr.size for arr in arrays)
        
        # Function to pad an array with its last value
        def pad_array(arr, target_length):
            if arr.size >= target_length:
                return arr
            else:
                padding_length = target_length - arr.size
                padding_value = arr[-1]  # Last value of the array
                return np.pad(arr, (0, padding_length), mode='constant', constant_values=padding_value)
        
        # Pad all arrays to the length of the longest array
        return np.vstack([pad_array(arr, max_length) for arr in arrays])

    if objfn_name is not None and objfn_list is None:
        objfn_list = [f'{objfn_name}' for nm in range(len(objective_fn))]

    if type(log_interv) is int:
        log_int_list = [log_interv]*len(objective_fn)
    elif type(log_interv) is list:
        log_int_list = log_interv
    else:
        print('*** log_interv must be an interger or a list')
        return

    plt.rcParams["figure.figsize"] = rcParams
    plt.rcParams["figure.dpi"] = dpi
    
    for c in range(len(objective_fn)):

        if objective_fn[c] is None or objective_fn[c] == []:
            continue
        else:
            select = resize_to_equal_and_pad(objective_fn[c]) # objective_fn[c] # 
            max_vals = smooth(np.nanmax(select, axis=0), smooth_weight)
            min_vals = smooth(np.nanmin(select, axis=0), smooth_weight)
            mean_vals = smooth(np.nanmean(select, axis=0), smooth_weight)
    
            if meas_min:
                lim = 'min'
                sel_val = min(mean_vals)
                sel_x = np.argmin(mean_vals)
            else:
                lim = 'max'
                sel_val = max(mean_vals)
                sel_x = np.argmax(mean_vals)
                
            sel_val = np.round(sel_val, prec) if prec is not None else sel_val
            sel_val_text = f'{sel_val}' if opt_format is None else f'{sel_val:{opt_format}}'
        
            xrange = [x * log_interv for x in range(select.shape[1])]
            plabel =  f'{lim}({meas_type}) = {sel_val_text} @ iter# {sel_x*log_int_list[c]}'
    
            if objfn_name is None:
                plt.plot(xrange, mean_vals, color = color[c])
            elif objfn_list is None:
                plt.plot(xrange, mean_vals, color = color[c], linestyle=linestyles[c], label=f'{objfn_name} {c}: {plabel}')
            else:
                plt.plot(xrange, mean_vals, color = color[c], linestyle=linestyles[c], label=f'{objfn_list[c]}: {plabel}')
            plt.fill_between(range(0, select.shape[1]), max_vals, min_vals, color = color[c], alpha = 0.2)
    
    if xlim is not None:
        plt.xlim(xlim[0], xlim[1])
    if ylim is not None:
        plt.ylim(ylim[0], ylim[1])

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    if objfn_name is not None:
        plt.legend(loc='best')

    if save_plot is not None:
        os.makedirs(os.path.dirname(save_plot), exist_ok=True)
        ext = os.path.splitext(save_plot)[1][1:]
        plt.savefig(save_plot, format=ext)
    plt.show()    
