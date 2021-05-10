# vim with YCM plugin container image

The image 

## run the container

``` shell
# Create and run in background
docekr run -d --name editor --restart always --env-file /path/to/.editor-envs -v /path/to/work:/work irikaq/vim-ycm -- tail -f /dev/null
# Start a bash to use vim
docker exec -it editor bash --login
```

## build image

``` shell
./build.sh
```
