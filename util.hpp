#ifndef UTIL_HPP
#define UTIL_HPP

#include <QtWebEngineWidgets>

const QJsonValue get_json_value(const QJsonObject, QLinkedList<QString>);

const QJsonObject to_json_obj(const QVariant);

const QJsonObject to_json_obj(const QJsonValue);

#endif // UTIL_HPP
