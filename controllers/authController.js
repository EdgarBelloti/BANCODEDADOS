const Usuario = require('../models/User');

exports.registrar = async (req, res) => {
  const { username, password } = req.body;
  try {
    if (!username || !password) {
      return res.status(400).send('Nome de usuário e senha são necessários.');
    }
    const usuarioExiste = await Usuario.findOne({ username });
    if (usuarioExiste) {
      return res.status(409).send('Nome de usuário já existe.');
    }
    const usuario = new Usuario({ username, password });
    await usuario.save();
    res.redirect('/api/auth/login');  // Alterado para usar o caminho completo
  } catch (error) {
    res.status(500).send(error.message);
  }
};

exports.login = async (req, res) => {
  const { username, password } = req.body;
  try {
    const usuario = await Usuario.findOne({ username, password });
    if (!usuario) {
      return res.redirect('/api/auth/registrar?msg=Falha%20no%20login.%20Usuário%20não%20encontrado%20ou%20senha%20incorreta.'); // Caminho completo
    }
    res.redirect('http://127.0.0.1:5000/');
  } catch (error) {
    res.status(500).send(error.message);
  }
};