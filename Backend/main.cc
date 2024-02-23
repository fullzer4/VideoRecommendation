#include <iostream>
#include <cpprest/http_listener.h>
#include <cpprest/json.h>

using namespace web;
using namespace web::http;
using namespace web::http::experimental::listener;

void handle_get(http_request request) {
    ucout << "Requisição GET recebida" << std::endl;

    json::value response;
    response[U("message")] = json::value::string(U("Olá, mundo!"));

    request.reply(status_codes::OK, response);
}

int main() {
    utility::string_t url = U("http://localhost:12345");
    http::uri_builder uri(url);
    auto addr = uri.to_uri().to_string();
    
    http_listener listener(addr);
    listener.support(methods::GET, handle_get);

    try {
        listener.open().then([&listener](){ ucout << "Servidor online" << std::endl; }).wait();
        std::cin.get();
        listener.close().then([&listener](){ ucout << "Servidor fechado" << std::endl; }).wait();
    } catch (const std::exception &e) {
        ucout << "Erro: " << e.what() << std::endl;
    }

    return 0;
}
