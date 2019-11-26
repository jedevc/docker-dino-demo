# Docker demo

Let's deploy a flask web app in Docker!

## Startup

First let's build our image!

    $ docker build . -t docker-dino

Now we can run it:

    $ docker run -d docker-dino
    69a3f27004e6c62c5227d594e87aa969b48eedf45448d6f62aaa7182f409371b
    $ docker ps
    CONTAINER ID        IMAGE              COMMAND                  CREATED             STATUS              PORTS               NAMES
    69a3f27004e6        docker-dino        "/bin/sh -c 'gunicor…"   14 seconds ago      Up 11 seconds       80/tcp              sharp_darwin

And we can now see our container is now running. But how can we actually
access it?

To do that, we can restart our container, but this time expose port 80 from
the container to port 8080 on our host!

    $ docker kill 69a3f27004e6
    69a3f27004e6
    $ docker run -p 8000:80 -d docker-dino 
    74470db53fe64cc0b457afb1ba6552145f267c698ddaa28624a62832812d1a16
    $ docker ps
    CONTAINER ID        IMAGE              COMMAND                  CREATED             STATUS                  PORTS                  NAMES
    74470db53fe6        docker-dino        "/bin/sh -c 'gunicor…"   2 seconds ago       Up Less than a second   0.0.0.0:8000->80/tcp   recursing_khorana

Now that the port is published, we can access our site:

    $ curl localhost:8000
    Hello World (and dinosaurs)!

## File uploads

Let's try and send a file to our website.

    $ curl http://localhost:8000/upload -F "file=@dino.txt"
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
    <title>500 Internal Server Error</title>
    <h1>Internal Server Error</h1>
    <p>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.</p>

Uh oh! We got an internal server error!

Docker lets us peek inside the container to have a look what's going on.

    $ docker logs 74470db53fe6
    [2019-11-21 16:27:54 +0000] [6] [INFO] Starting gunicorn 20.0.0
    [2019-11-21 16:27:54 +0000] [6] [INFO] Listening at: http://0.0.0.0:80 (6)
    [2019-11-21 16:27:54 +0000] [6] [INFO] Using worker: sync
    [2019-11-21 16:27:54 +0000] [10] [INFO] Booting worker with pid: 10
    [2019-11-21 16:28:08,911] ERROR in app: Exception on /upload [POST]
    Traceback (most recent call last):
    ...
    File "/app/dino/dino.py", line 27, in upload
        file.save(os.path.join(UPLOADS, out_filename))
    ...
    FileNotFoundError: [Errno 2] No such file or directory: '/app/uploads/dino.txt'

Aha! The directory we're trying to upload files to doesn't exist!

We'll fix this later in the Dockerfile, but for now, we'll use another
technique to patch the container while it's running!

    $ docker exec -it 74470db53fe6 /bin/bash
    root@74470db53fe6:/app# ls
    Pipfile  Pipfile.lock  README.md  demo
    root@74470db53fe6:/app# mkdir uploads

Now we want to exit the container with ctrl-d and we can try the upload again:

    $ curl http://localhost:8000/upload -F "file=@demo.txt"
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
    <title>Redirecting...</title>
    <h1>Redirecting...</h1>
    <p>You should be redirected automatically to target URL: <a href="/files/dino.txt">/files/dino.txt</a>.  If not click the link.

Great! We should then be able to easily get the dinosaur:

    $ curl http://localhost:8000/dinos/dino.txt
           __
          /oo\
         |    |
     ^^  (vvvv)   ^^
     \\  /\__/\  //
      \\/      \//
       /        \        
      |          |    ^  
      /          \___/ | 
     (            )     |
      \----------/     /
        //    \\_____/
       W       W 

We can then patch our Dockerfile for future containers:

```Dockerfile
...
ENV UPLOADS_DIR=uploads/
RUN mkdir -p uploads/
...
```
