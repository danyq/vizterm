#!/usr/bin/env python3
#
# http://github.com/danyq/vizterm
#
# Python library for use with vizterm.
# Defines a new print() function to handle visual content.

import os
import io
import inspect
import builtins
import base64
import json
import pprint
import socket
import time

def tick():
    '''convenience function: print the current line number'''
    frameinfo = inspect.getframeinfo(inspect.currentframe().f_back)
    print('%s:%i' % (frameinfo.filename, frameinfo.lineno))

vizterm_socket = None
def vizport(port):
    '''output to the given port number instead of stdout.
    vizterm can receive from a network port like this:
    vizterm nc -kl localhost <port>'''
    global vizterm_socket
    if port is None:
        vizterm_socket = None
        return
    vizterm_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        vizterm_socket.connect(('localhost', port))
        clear()
        builtins.print('vizprint: sending output to port %i' % port)
    except ConnectionRefusedError:
        builtins.print('vizprint: connection refused on port %i. using stdout.' % port)
        vizterm_socket = None

def clear():
    output_json({'type':'clear'})

def output_json(x):
    if vizterm_socket:
        vizterm_socket.send(('json %s\n' % json.dumps(x)).encode())
    else:
        builtins.print('json %s' % json.dumps(x))
    return True

def output_html(x, attr):
    return output_json({'type':'html', 'data':x, **attr})

def output_str(x, attr):
    if type(x) is not str: return False
    return output_json({'type':'str', 'data':x, **attr})

def output_block(x, attr):
    if type(x) is not str: return False
    return output_json({'type':'block', 'data':x, **attr})

def output_img(x, attr):
    if 'Image' not in type(x).__name__: return False
    if not hasattr(x, 'save'): return False
    buf = io.BytesIO()
    x.save(buf, format='JPEG')
    img_str = base64.b64encode(buf.getvalue()).decode()
    return output_html('<img src="data:image/jpeg;base64,%s">' % img_str, attr)

def output_plt(plt, attr):
    if not hasattr(plt, 'savefig'): return False
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    img_str = base64.b64encode(buf.getvalue()).decode()
    return output_html('<img src="data:image/png;base64,%s">' % img_str, attr)

def output_repr(x, attr):
    if not hasattr(x, '_repr_html_'): return False
    return output_html(x._repr_html_(), attr)

def print(*args, sep=' ', end='\n', id=None, **attr):
    if 'file' in attr or ('VIZTERM' not in os.environ and vizterm_socket is None):
        return builtins.print(*args, sep=sep, end=end, **attr)

    if args:
        entries = []
        for arg in args:
            entries.append(arg)
            entries.append(sep)
        entries[-1] = end
    else:
        entries = [end]

    for i,x in enumerate(entries):
        if id: attr['id'] = '%s:%i' % (str(id), i)
        if output_img(x, attr): continue
        if output_plt(x, attr): continue
        if output_repr(x, attr): continue
        if output_str(x, attr): continue
        if type(x) is map: x = list(x)
        ppargs = { k:attr[k] for k in ('indent','width','depth','compact') if k in attr }
        ppstr = pprint.pformat(x, **ppargs)
        if '\n' in ppstr:
            output_block(ppstr, attr)
        else:
            output_str(ppstr, attr)  # better text alignment
