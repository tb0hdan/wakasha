.PHONY: snowboy

snowboy:
	@cd snowboy/swig/Python; make
	@cp -v snowboy/swig/Python/*.so wakasha/extlib/snowboydetect/
	@cp -v snowboy/swig/Python/*.py wakasha/extlib/snowboydetect/
	@cp -v snowboy/examples/Python/*.py wakasha/extlib/snowboydetect/
	@cp -R snowboy/resources wakasha/extlib/snowboydetect

deps:	snowboy
	@pip install -r requirements.txt

py2app:
	@python setup.py py2app

clean:
	@rm -rf ./build ./dist