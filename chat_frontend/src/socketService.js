import React, {useEffect} from 'react';
import openSocket from 'socket.io-client';

const SOCKET_URL = 'localhost:8080';
let socket;

const SocketService = () => {

    const configureSocket = () => {
        socket = openSocket(SOCKET_URL);
        socket.on("command", (data) => {
            console.log(data);
        });
    };

    useEffect(configureSocket, []);

    return <></>;
};

const sendSocket = data => {
    socket.emit("command", {type: data.type, id: data.id, content: data.content});
};

export default SocketService;