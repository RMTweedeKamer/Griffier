# Deploy

```
$ # Create directory for app
$ mkdir ~/griffier
$ ls
$ # outputs settings.json and config.json
$ docker build https://github.com/RMTweedeKamer/Griffier.git -t griffier
$ docker run -v $PWD/config.json:/griffier/config.json -v $PWD/settings.json:/griffier/data/settings.json --name griffier --restart unless-stopped griffier
```
