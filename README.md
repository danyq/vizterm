
## Usage

`vizterm <cmd>` starts a web server at <http://localhost:8080/>. When that page is loaded, it runs the given command and shows the output in the browser.

The vizprint python library provides a custom `print()` function that makes images and plots displayable in `vizterm`:

    from vizprint import print

To show a PIL image, just print it:

    im = Image.open('image.jpg')
    print(im)

To show a pyplot, print the pyplot object or figure. You don't need to call `plt.show()`.

    plt.plot([1,2,3])
    print(plt)

See the example:

    $ vizterm ./example.py

To re-run the command, you don't need to exit vizterm. Just reload the page.


## Interactive programs

For use with interactive commands or debuggers, vizterm can work over a socket rather than stdout. First start the server using netcat to listen on a port:

    $ vizterm nc -kl localhost 9999

Then in python, call `vizport()` to open a connection. Future output will be sent to that port instead of stdout.

    from vizprint import print, vizport
    vizport(9999)
    print(...)

You'll need to load the webpage first to start netcat. Then, run your code normally.

## Requirements

vizterm requires python3. It works with Pillow/PIL, matplotlib, and any IPython-integrated libraries that implement `_repr_html_`.
