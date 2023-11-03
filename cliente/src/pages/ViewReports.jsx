import React, { useState, useEffect } from 'react';
import { TextField, Button } from '@mui/material';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Link } from 'react-router-dom';

const darkTheme = createTheme({
    palette: {
      mode: 'dark',
    },
  });

function ViewReports() {
    const [imageNames, setImageNames] = useState([]);

    useEffect(() => {
        fetch('http://127.0.0.1:8000/get_all_images')
            .then(response => response.json())
            .then(data => {
                const imageNames = data.images;
                setImageNames(imageNames);
            })
            .catch(error => {
                console.error('Error al obtener la lista de imágenes:', error);
            });
    }, []);

    return (
        <ThemeProvider theme={darkTheme}>
        <CssBaseline />
        <div style={{ width: "80%",  padding: 10, margin: "auto", marginTop: 50, marginLeft: 150 }}>
            <h1>Reportes</h1>

            {imageNames.map((imageName, index) => (
                <div key={index}>
                    <h2>Imagen {index + 1}</h2>
                    <img
                        src={`http://127.0.0.1:8000/get_image/${imageName}`}
                        alt={`Reporte ${index + 1}`}
                    />
                </div>
            ), [])}
            <Link to="/login">
            <Button variant="contained" color="warning">Regresar</Button>
        </Link>
        </div>
        
        </ThemeProvider>
    );
            }

export default ViewReports;

