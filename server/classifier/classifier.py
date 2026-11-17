import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

from server.classifier.classifier_static.classifier import check_static
from server.classifier.classifier_medicine.classifier import check_medicine
from server.classifier.classifier_egida.classifier import check_main



logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s [%(name)s] %(message)s'
)
logger = logging.getLogger(__name__)


class ClassifierManager:
    def __init__(self):
        # Список доменов, каждая функция в качестве аргумента получает промпт, возвращает вердикт
        self._classifiers = {
            "static": check_static,
            "medicine": check_medicine,
            "egida": check_main
        }


    def classify(self, name, content):
        if name not in self._classifiers:
            raise ValueError(f"Unknown classifier: {name}")
        return self._classifiers[name](content)

    def classify_multiple(self, names, content):
        results = {}
        static_result = self.classify('static', content)
        if static_result:
            return {'static': static_result}
        with ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(self._classifiers[name], content): name
                for name in names
                if name in self._classifiers
            }

            for future in as_completed(futures):
                name = futures[future]
                try:
                    result = future.result()
                except Exception as e:
                    logger.error('Classifier error', exc_info=e)
                    result = None
                results[name] = result

        #TODO: raise Error if all Nones
        return results

    def available_classifiers(self):
        return list(self._classifiers.keys())
