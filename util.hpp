#ifndef UTIL_HPP
#define UTIL_HPP

#include <QtWebEngineWidgets>

const QJsonValue get_value(const QJsonObject, QLinkedList<QString>);
const QJsonObject to_json_obj(const QVariant);
const QJsonObject to_json_obj(const QJsonValue);

const QJsonValue get_value(const QJsonObject json_obj, QLinkedList<QString> keys) {

	QJsonValue obj = json_obj.value(keys.takeFirst());
	while(!keys.isEmpty()) {
		obj = obj.toObject().value(keys.takeFirst());
	}

	return obj;
}

const QJsonObject to_json_obj(const QVariant raw_json) {

	QJsonDocument json_doc(raw_json.toJsonObject());
	return json_doc.object();
}

const QJsonObject to_json_obj(const QJsonValue json_val) {

	return json_val.toObject();
}

#endif // UTIL_HPP
