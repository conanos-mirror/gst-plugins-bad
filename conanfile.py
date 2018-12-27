from conans import ConanFile, Meson, tools
from conanos.build import config_scheme
import os

class GstpluginsbadConan(ConanFile):
    name = "gst-plugins-bad"
    version = "1.14.4"
    description = "'Bad' GStreamer plugins and helper libraries"
    url = "https://github.com/conanos/gst-plugins-bad/"
    homepage = "https://github.com/GStreamer/gst-plugins-bad"
    license = "GPL-v2"
    generators = "gcc","visual_studio"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        'fPIC': [True, False]
    }
    default_options = { 'shared': True, 'fPIC': True }

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx

        config_scheme(self)

    def requirements(self):
        self.requires.add("gstreamer/1.14.4@conanos/stable")
        self.requires.add("gst-plugins-base/1.14.4@conanos/stable")
        self.requires.add("bzip2/1.0.6@conanos/stable")
        self.requires.add("libass/0.14.0-13@conanos/stable")
        self.requires.add("faad2/2.8.8@conanos/stable")
        self.requires.add("libkate/0.4.1@conanos/stable")
        self.requires.add("zlib/1.2.11@conanos/stable")
        self.requires.add("openh264/1.8.0@conanos/stable")
        self.requires.add("opus/1.2.1@conanos/stable")
        self.requires.add("nettle/3.4.1@conanos/stable")
        self.requires.add("librtmp/2.4.r512-1@conanos/stable")
        self.requires.add("libsrtp/2.2.0@conanos/stable")
        self.requires.add("libdca/0.0.6@conanos/stable")
        self.requires.add("libnice/0.1.14@conanos/stable")
        self.requires.add("soundtouch/2.1.2@conanos/stable")
        self.requires.add("librsvg/2.40.20@conanos/stable")
        self.requires.add("openjpeg/2.3.0@conanos/stable")
        self.requires.add("openssl/1.1.1@conanos/stable")
        self.requires.add("spandsp/0.0.6@conanos/stable")
    
    def build_requirements(self):
        self.build_requires("glib/2.58.1@conanos/stable")

    def source(self):
        remotes = {'origin': 'https://github.com/GStreamer/gst-plugins-bad.git'}
        extracted_dir = self.name + "-" + self.version
        tools.mkdir(extracted_dir)
        with tools.chdir(extracted_dir):
            self.run('git init')
            for key, val in remotes.items():
                self.run("git remote add %s %s"%(key, val))
            self.run('git fetch --all')
            self.run('git reset --hard %s'%(self.version))
            self.run('git submodule update --init --recursive')
        os.rename(extracted_dir, self._source_subfolder)

    def build(self):
        deps=["gstreamer","gst-plugins-base","bzip2","libass","faad2","libkate","zlib","openh264","opus","nettle",
              "librtmp","libsrtp","libdca","libnice","soundtouch","librsvg","openjpeg","openssl","spandsp","glib"]
        pkg_config_paths=[ os.path.join(self.deps_cpp_info[i].rootpath, "lib", "pkgconfig") for i in deps ]
        prefix = os.path.join(self.build_folder, self._build_subfolder, "install")
        defs = {'prefix' : prefix}
        if self.settings.os == "Linux":
            defs.update({'libdir':'lib'})
        if self.settings.os == "Windows":
            defs.update({'disable_introspection':'true'})

        meson = Meson(self)
        if self.settings.os == 'Windows':
                meson.configure(defs=defs,source_dir=self._source_subfolder, build_dir=self._build_subfolder,
                                pkg_config_paths=pkg_config_paths)
                meson.build()
                self.run('ninja -C {0} install'.format(meson.build_dir))

    def package(self):
        pass

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

