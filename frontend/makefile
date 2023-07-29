package-lock.json: package.json
	npm install
	touch node_modules/.develop

node_modules/.develop: package.json package-lock.json
	npm install
	touch node_modules/.develop

.PHONY: develop
develop: node_modules/.develop

.PHONY: run
run:
	npm run dev
