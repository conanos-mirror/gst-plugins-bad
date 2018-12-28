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
        #self.requires.add("librsvg/2.40.20@conanos/stable")
        self.requires.add("openjpeg/2.3.0@conanos/stable")
        self.requires.add("openssl/1.1.1@conanos/stable")
        self.requires.add("spandsp/0.0.6@conanos/stable")
        self.requires.add("orc/0.4.28@conanos/stable")
        self.requires.add("pango/1.42.4@conanos/stable")
    
    def build_requirements(self):
        self.build_requires("glib/2.58.1@conanos/stable")
        self.build_requires("libffi/3.299999@conanos/stable")
        self.build_requires("gdk-pixbuf/2.38.0@conanos/stable")
        self.build_requires("cairo/1.15.12@conanos/stable")
        self.build_requires("libpng/1.6.34@conanos/stable")
        self.build_requires("pixman/0.34.0@conanos/stable")
        self.build_requires("fontconfig/2.13.0@conanos/stable")
        self.build_requires("freetype/2.9.1@conanos/stable")
        if self.settings.os == "Windows":
            self.build_requires("expat/2.2.5@conanos/stable")
        self.build_requires("libcroco/0.6.12@conanos/stable")
        self.build_requires("libxml2/2.9.8@conanos/stable")
        self.build_requires("libiconv/1.15@conanos/stable")
        self.build_requires("libtiff/4.0.10@conanos/stable")
        self.build_requires("harfbuzz/2.1.3@conanos/stable")
        self.build_requires("fribidi/1.0.5@conanos/stable")

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
        #"librsvg",
        deps=["gstreamer","gst-plugins-base","bzip2","libass","faad2","libkate","zlib","openh264","opus","nettle",
              "librtmp","libsrtp","libdca","libnice","soundtouch","openjpeg","openssl","spandsp",
              "orc","glib","libffi","gdk-pixbuf","cairo","libpng","pixman","fontconfig","freetype","expat","pango","libcroco","libxml2","libiconv","harfbuzz","fribidi"]
        pkg_config_paths=[ os.path.join(self.deps_cpp_info[i].rootpath, "lib", "pkgconfig") for i in deps ]
        prefix = os.path.join(self.build_folder, self._build_subfolder, "install")
        binpath = [ os.path.join(self.deps_cpp_info[i].rootpath, "bin") for i in ["orc","glib"]  ]
        include = [ os.path.join(self.deps_cpp_info["cairo"].rootpath, "include"),
                    os.path.join(self.deps_cpp_info["cairo"].rootpath, "include","cairo"),
                    #os.path.join(self.deps_cpp_info["librsvg"].rootpath, "include","librsvg-2.0"),
                    os.path.join(self.deps_cpp_info["gdk-pixbuf"].rootpath, "include","gdk-pixbuf-2.0"),
                    os.path.join(self.deps_cpp_info["libxml2"].rootpath, "include","libxml2"),
                    os.path.join(self.deps_cpp_info["libiconv"].rootpath, "include"),
                    os.path.join(self.deps_cpp_info["pango"].rootpath, "include","pango-1.0"), ]

        defs = {'prefix' : prefix}
        if self.settings.os == "Linux":
            defs.update({'libdir':'lib'})
        if self.settings.os == "Windows":
            defs.update({'disable_introspection':'true'})

        meson = Meson(self)
        if self.settings.os == 'Windows':
            with tools.environment_append({
                'PATH' : os.pathsep.join(binpath + [os.getenv('PATH')]),
                'INCLUDE' : os.pathsep.join(include + [os.getenv('INCLUDE')]),
                }):
                meson.configure(defs=defs,source_dir=self._source_subfolder, build_dir=self._build_subfolder,
                                pkg_config_paths=pkg_config_paths)
                meson.build()
                self.run('ninja -C {0} install'.format(meson.build_dir))

    def package(self):
        self.copy("*", dst=self.package_folder, src=os.path.join(self.build_folder,self._build_subfolder, "install"))

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

