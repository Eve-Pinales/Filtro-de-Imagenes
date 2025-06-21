#include <opencv2/opencv.hpp>
#include <iostream>

using namespace std;
using namespace cv;

// .vscode/c_cpp_properties.json
{
    "configurations": [
        {
            "includePath": [
                "${workspaceFolder}/**",
                "C:/path/to/opencv/build/include"
            ],
            ...
        }
    ],
    ...
}

void aplicarGrises(Mat& img) {
    cvtColor(img, img, COLOR_BGR2GRAY);
}

void aplicarInversion(Mat& img) {
    bitwise_not(img, img);
}

void aplicarDesenfoque(Mat& img) {
    GaussianBlur(img, img, Size(9, 9), 0);
}

void aplicarBinarizacion(Mat& img) {
    cvtColor(img, img, COLOR_BGR2GRAY);
    threshold(img, img, 128, 255, THRESH_BINARY);
}

void aplicarRotacion(Mat& img) {
    rotate(img, img, ROTATE_90_CLOCKWISE);
}

int main(int argc, char** argv) {
    if (argc < 2) {
        cout << "Uso: ./editor imagen.jpg" << endl;
        return 1;
    }

    Mat imagen = imread(argv[1]);
    if (imagen.empty()) {
        cout << "No se pudo abrir la imagen." << endl;
        return 1;
    }

    cout << "Opciones:\n1. Grises\n2. Inversión\n3. Desenfoque\n4. Binarización\n5. Rotación\nOpción: ";
    int opcion;
    cin >> opcion;

    switch (opcion) {
        case 1: aplicarGrises(imagen); break;
        case 2: aplicarInversion(imagen); break;
        case 3: aplicarDesenfoque(imagen); break;
        case 4: aplicarBinarizacion(imagen); break;
        case 5: aplicarRotacion(imagen); break;
        default: cout << "Opción inválida." << endl; return 1;
    }

    imshow("Resultado", imagen);
    waitKey(0);
    imwrite("resultado.png", imagen);
    cout << "Imagen guardada como resultado.png" << endl;

    return 0;
}
