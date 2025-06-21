
package gui;

import filtros.*;
import modelo.Imagen;

import javax.swing.*;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import javax.imageio.ImageIO;

public class EditorGUI extends JFrame {
    private Imagen editor = new Imagen();
    private JLabel labelImagen = new JLabel();

    public EditorGUI() {
        setTitle("Editor de Imágenes en Java");
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setLayout(new BorderLayout());

        JPanel panelBotones = new JPanel(new GridLayout(0, 1));

        addBoton(panelBotones, "Cargar Imagen", () -> cargarImagen());
        addBoton(panelBotones, "Grises", () -> aplicarFiltro(new FiltroGrises()));
        addBoton(panelBotones, "Inversión", () -> aplicarFiltro(new FiltroInversion()));
        addBoton(panelBotones, "Binarización", () -> aplicarFiltro(new FiltroBinarizacion()));
        addBoton(panelBotones, "Rotar", () -> aplicarFiltro(new FiltroRotacion()));
        addBoton(panelBotones, "Guardar Imagen", () -> guardarImagen());

        add(panelBotones, BorderLayout.WEST);
        add(labelImagen, BorderLayout.CENTER);

        setSize(800, 600);
        setVisible(true);
    }

    private void addBoton(JPanel panel, String texto, Runnable accion) {
        JButton boton = new JButton(texto);
        boton.addActionListener(e -> accion.run());
        panel.add(boton);
    }

    private void cargarImagen() {
        JFileChooser chooser = new JFileChooser();
        if (chooser.showOpenDialog(this) == JFileChooser.APPROVE_OPTION) {
            editor.cargar(chooser.getSelectedFile().getAbsolutePath());
            actualizarVista();
        }
    }

    private void guardarImagen() {
        JFileChooser chooser = new JFileChooser();
        if (chooser.showSaveDialog(this) == JFileChooser.APPROVE_OPTION) {
            editor.guardar(chooser.getSelectedFile().getAbsolutePath());
        }
    }

    private void aplicarFiltro(Filtro f) {
        if (editor.getImagen() != null) {
            editor.setImagen(f.aplicar(editor.getImagen()));
            actualizarVista();
        }
    }

    private void actualizarVista() {
        BufferedImage img = editor.getImagen();
        if (img != null) {
            ImageIcon icon = new ImageIcon(img.getScaledInstance(400, -1, Image.SCALE_SMOOTH));
            labelImagen.setIcon(icon);
        }
    }
}
