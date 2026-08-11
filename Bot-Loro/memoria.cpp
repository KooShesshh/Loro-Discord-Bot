#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <cctype>
#include <fstream>

class Mensaje {
public:
    std::string user_id;
    std::string contenido;
    long long timestamp;
};

std::string convertir_mensaje(std::string texto) {
    std::transform(texto.begin(), texto.end(), texto.begin(),
               [](unsigned char c){ return std::tolower(c); });
    return texto;
}

class Personalidad {
public:
    float amable   = 0.5f;
    float bromista = 0.3f;
    float grosero  = 0.2f;

    void reaccionar(const std::string& mensaje) {
        std::string msg = convertir_mensaje(mensaje);
           if(msg.find("gracias") != std::string::npos ||
            msg.find("por favor") != std::string::npos) {
            amable += 0.05f;
            grosero -= 0.08f;
        }

        if(msg.find("idiota") != std::string::npos ||
            msg.find("estupido") != std::string::npos) {
            amable  -= 0.08f;
            grosero += 0.06f;
        }

        if(msg.find("era una broma") != std::string::npos ||
            msg.find("jaja") != std::string::npos) {
            bromista += 0.04f;
            grosero  -= 0.05f;
            amable   -= 0.03f;
        }

        if(amable > 1.0f) amable = 1.0f;
        if(amable < 0.0f) amable = 0.0f;
        if(bromista > 1.0f) bromista = 1.0f;
        if(bromista < 0.0f) bromista = 0.0f;
        if(grosero > 1.0f) grosero = 1.0f;
        if(grosero < 0.0f) grosero = 0.0f;
    }
    void mostrar() const {
    std::cout << "AMABLE:" << amable 
              << " BROMISTA:" << bromista 
              << " GROSERO:" << grosero << std::endl;
    }
};

void agregar_mensaje(std::vector<Mensaje>& historial, const Mensaje& nuevo) {
    historial.push_back(nuevo);
}

void guardar_historial(const std::vector<Mensaje>& historial) {
    std::ofstream mis_palabras("mis_palabras.txt");
    if(mis_palabras.is_open()) {
        for(int i = 0; i < historial.size(); i++) {
            mis_palabras << historial[i].user_id << "|" << historial[i].contenido << std::endl;
}
mis_palabras.close();
    }
    else {
        return;
    }
}

void cargar_historial(std::vector<Mensaje>& historial) {
    std::ifstream archivo("mis_palabras.txt");
    if(!archivo.is_open()) {
        return;
    }

    std::string linea;

    while (std::getline(archivo, linea)) {
        size_t posicion = linea.find('|');
        if(posicion != std::string::npos) {
            Mensaje m;
            m.user_id = linea.substr(0, posicion);
            m.contenido = linea.substr(posicion + 1);
            historial.push_back(m);
          }
    }

    archivo.close();
}

void guardar_personalidad(const Personalidad& bot) {
    std::ofstream personalidad("personalidad.txt");
    if(personalidad.is_open()) {
    personalidad << bot.amable << std::endl;
    personalidad << bot.bromista << std::endl;
    personalidad << bot.grosero << std::endl;
    personalidad.close();
    }
    else {
        return;
    }
}

void cargar_personalidad(Personalidad& bot) {
    std::ifstream personalidad("personalidad.txt");
    if(personalidad.is_open()) {
    personalidad >> bot.amable;
    personalidad >> bot.bromista;
    personalidad >> bot.grosero;
    personalidad.close();
    }
    else {
        return;
    }
}

int main() {
    Personalidad bot;
    cargar_personalidad(bot);

    std::vector<Mensaje> historial;
    cargar_historial(historial);

    Mensaje m;
    m.user_id = "discord_user";

    std::getline(std::cin, m.contenido);

    agregar_mensaje(historial, m);
    bot.reaccionar(m.contenido);

    guardar_personalidad(bot);
    guardar_historial(historial);

    bot.mostrar();

    return 0;
}
