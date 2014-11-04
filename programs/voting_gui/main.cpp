#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>

#include "ClientWrapper.hpp"

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);

    ClientWrapper* client = new ClientWrapper(&app);
    client->initialize();

    QQmlApplicationEngine engine;
    QQmlContext* context = engine.rootContext();
    context->setContextProperty("bitshares", client);
    engine.load(QUrl(QStringLiteral("qrc:/qml/main.qml")));

    return app.exec();
}