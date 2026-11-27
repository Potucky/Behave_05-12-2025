.PHONY: test smoke unit allure

BEHAVE = behave --no-color -f pretty -o - -f allure_behave.formatter:AllureFormatter -o reports/allure-results

test: unit
	$(BEHAVE)

smoke: unit
	$(BEHAVE) --tags=@smoke

unit:
	python -m unittest discover -s framework -p "test_*.py"

allure:
	allure generate reports/allure-results --clean -o reports/allure-report
