const express = require('express');
const router = express.Router();
const path = require('path');
const authController = require('../controllers/authController');

// Rota GET para servir a página de login
router.get('/login', (req, res) => {
  res.sendFile(path.join(__dirname, '../views/login.html'));
});

router.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '../views/login.html'));
});

// Rota GET para servir a página de cadastro
router.get('/registrar', (req, res) => {
  res.sendFile(path.join(__dirname, '../views/registrar.html'));
});

// Rota POST para registrar
router.post('/registrar', authController.registrar);

// Rota POST para login
router.post('/login', authController.login);

module.exports = router;
