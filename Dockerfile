# Dockerfile with nginx base image

FROM nginx

# label is a good practice, though optional
LABEL MAINTAINER = scutrupi@spartaglobal.com

# copy the index file
COPY ./app1/index.html /usr/share/nginx/html

# incoming port
EXPOSE 80

# shell command
CMD ["nginx", "-g", "daemon off;"]



