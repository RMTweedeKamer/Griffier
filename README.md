# Deploy

```
$ # Create directory for app
$ mkdir ~/griffier
$ ls
$ # outputs settings.json and config.json
$ docker build https://github.com/RMTweedeKamer/Griffier.git -t griffier
$ docker run -v $PWD/config.json:/griffier/config.json -v $PWD/settings.json:/griffier/data/settings.json --name griffier --restart unless-stopped griffier
```

# Redeploy on VPS

```
$ cd ~/apps/Griffier
$ docker build https://github.com/RMTweedeKamer/Griffier.git -t griffier
$ docker stop griffier
$ docker rm griffier
$ docker run -v $PWD/config.json:/griffier/config.json -v $PWD/settings.json:/griffier/data/settings.json --name griffier --restart unless-stopped griffier

$ # or Griffier Development

$ cd ~/apps/GriffierTest
$ docker build https://github.com/RMTweedeKamer/Griffier.git -t griffier-test
$ docker stop griffier-test
$ docker rm griffier-test
$ docker run -v $PWD/config.json:/griffier/config.json -v $PWD/settings.json:/griffier/data/settings.json --name griffier-test --restart unless-stopped griffier-test
```
