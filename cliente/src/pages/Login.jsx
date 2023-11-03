import React, { useState } from 'react';
import { TextField, Button } from '@mui/material';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Link } from 'react-router-dom';

const darkTheme = createTheme({
    palette: {
      mode: 'dark',
    },
  });
  
  
function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [idparticion, setIdparticion] = useState('');

    const handleIDparticionChange = (event) => {
        setIdparticion(event.target.value);
    };

    const handleUsernameChange = (event) => {
        setUsername(event.target.value);
    };

    const handlePasswordChange = (event) => {
        setPassword(event.target.value);
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        console.log(`Username: ${username}, Password: ${password}`);
        // Add your login logic here
    };

    const handleButtonClick = async (e) => {
        e.preventDefault();

        // Realiza una solicitud POST al servidor Flask para el inicio de sesión
        try {
          const response = await fetch('http://127.0.0.1:8000/login', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 'username': username, 'password': password, 'id': idparticion }),
          });
    
          if (response.status === 200) {
            // Redirige al usuario a la URL de destino después del inicio de sesión exitoso
            window.location.href = 'http://localhost:5173/view-reports';
          } else {
            // Maneja el caso en que las credenciales sean incorrectas u ocurra un error
            console.log('Inicio de sesión fallido');
          }
        } catch (error) {
          console.error('Error al iniciar sesión:', error);
        }
    }

    return (
        <ThemeProvider theme={darkTheme}>
        <CssBaseline />
        <div style={{ width: "80%",  padding: 10, margin: "auto", marginTop: 300, marginLeft: 800 }}>
        <form onSubmit={handleSubmit}>
            <TextField
                label="ID particion"
                value={idparticion}
                onChange={handleIDparticionChange}
                margin="normal"
                variant="outlined"
            />
            <br /> 
            <TextField
                label="User"
                value={username}
                onChange={handleUsernameChange}
                margin="normal"
                variant="outlined"
            />
            <br /> 
            <TextField
                label="Password"
                type="password"
                value={password}
                onChange={handlePasswordChange}
                margin="normal"
                variant="outlined"
            />
            <br /> <br /> <br />
            <Button type="submit" variant="contained" color="primary" onClick={handleButtonClick}>
                Login
            </Button>
        </form>
        <br /> <br /> <br /> <br /> <br /> <br />

        <Link to="/">
            <Button variant="contained" color="warning">Regresar</Button>
        </Link>
        </div>
    </ThemeProvider>
    );
}

export default Login;
