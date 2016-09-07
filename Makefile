.PHONY: snowboy

snowboy:
	@cd snowboy/swig/Python; make
	@mkdir -p wakasha/extlib/snowboydetect/
	@cp -v snowboy/swig/Python/*.so wakasha/extlib/snowboydetect/
	@cp -v snowboy/swig/Python/*.py wakasha/extlib/snowboydetect/
	@cp -v snowboy/examples/Python/*.py wakasha/extlib/snowboydetect/
	@cp -v model.pmdl wakasha/extlib/snowboydetect/resources/
	@cp -R snowboy/resources wakasha/extlib/snowboydetect

deps:	snowboy
	@pip install -r requirements.txt

py2app:
	@python setup.py py2app

dmg:	py2app
	@hdiutil create -srcfolder dist/wakasha.app ./wakasha.dmg

clean:
	@rm -rf ./build ./dist
	@rm -f ./*.dmg
