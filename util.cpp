#include "util.hpp"

const QJsonValue get_json_value(const QJsonObject json_obj, QLinkedList<QString> keys) {

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
