# HomeSweetHome

HomeSweetHome is a library providing opinionated home directory and Dynaconf-based configuration for Python projects.

## Usage

Let's say that your application is named `myapp`.

By default HomeSweetHome assumes your application directory is `~/.myapp` and that default configuration file for your application is a YML file `~/.myapp/myapp.yml`. In order to make sure the following structure is in place, just create `SweetHome` object.

```python
from homesweethome.homesweethome import SweetHome

sweet_home = SweetHome("myapp")
```

Now you can read properties from the configuration YML: 

```python
from homesweethome.homesweethome import SweetHome

sweet_home = SweetHome("myapp")
host = sweet_home.read_setting("server.host")
port = sweet_home.read_setting("server.port")
```
