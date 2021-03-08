from conans import ConanFile, CMake, tools


class ZLMediaKitConan(ConanFile):
    name = "ZLMediaKit"
    version = "5.0"
    license = "MIT"
    author = "xia-chu"
    url = "https://github.com/xia-chu/ZLMediaKit"
    description = "A lightweight RTSP/RTMP/HTTP/HLS/HTTP-FLV/WebSocket-FLV/HTTP-TS/HTTP-fMP4/WebSocket-TS/WebSocket-fMP4/GB28181 server and client framework based on C++11"
    topics = ("http", "rtsp", "mp4", "hls", "rtmp", "websocket", "flv", "ts", "http-flv", "gb28181", "websocket-flv", "http-ts", "http-fmp4", "websocket-fmp4", "websocket-ts")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = "cmake", "cmake_find_package", "cmake_paths"
    requires = ["ZLToolKit/4.0", "libx264/20191217"]

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        self.run("git clone https://gitee.com/xia-chu/ZLMediaKit.git")
        self.run("git clone https://gitee.com/xia-chu/media-server.git")
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("ZLMediaKit/CMakeLists.txt", "project(ZLMediaKit)",
                              '''project(ZLMediaKit)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
include(${CMAKE_BINARY_DIR}/conan_paths.cmake)
set(CMAKE_MODULE_PATH ${CMAKE_BINARY_DIR} ${CMAKE_MODULE_PATH})''')

        tools.replace_in_file("ZLMediaKit/CMakeLists.txt", "set(ToolKit_Root ${CMAKE_CURRENT_SOURCE_DIR}/3rdpart/ZLToolKit/src)", '''#set(ToolKit_Root ${CMAKE_CURRENT_SOURCE_DIR}/3rdpart/ZLToolKit/src)''')
        tools.replace_in_file("ZLMediaKit/CMakeLists.txt", "INCLUDE_DIRECTORIES(${ToolKit_Root})", '''#INCLUDE_DIRECTORIES(${ToolKit_Root})''')
        tools.replace_in_file("ZLMediaKit/CMakeLists.txt", "set(MediaServer_Root ${CMAKE_CURRENT_SOURCE_DIR}/3rdpart/media-server)", '''set(MediaServer_Root ${CMAKE_CURRENT_SOURCE_DIR}/../media-server)''')
        tools.replace_in_file("ZLMediaKit/CMakeLists.txt", "INCLUDE_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR}/3rdpart)", '''INCLUDE_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR}/3rdpart)
            INCLUDE_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR}/../)''')
        tools.replace_in_file("ZLMediaKit/CMakeLists.txt", "add_library(zltoolkit STATIC ${ToolKit_src_list})", '''#add_library(zltoolkit STATIC ${ToolKit_src_list})''')
        tools.replace_in_file("ZLMediaKit/CMakeLists.txt", "set(LINK_LIB_LIST zlmediakit zltoolkit)", '''set(LINK_LIB_LIST zlmediakit ${CONAN_LIBS})''')
        tools.replace_in_file("ZLMediaKit/CMakeLists.txt", "set_target_properties(zltoolkit PROPERTIES COMPILE_FLAGS ${VS_FALGS} )", '''#set_target_properties(zltoolkit PROPERTIES COMPILE_FLAGS ${VS_FALGS} )''')
        tools.replace_in_file("ZLMediaKit/CMakeLists.txt", "add_subdirectory(api)", '''#add_subdirectory(api)''')
        tools.replace_in_file("ZLMediaKit/CMakeLists.txt", "add_subdirectory(tests)", '''#add_subdirectory(tests)''')
        tools.replace_in_file("ZLMediaKit/CMakeLists.txt", "add_subdirectory(server)", '''#add_subdirectory(server)''')

        if self.options.shared:
        	tools.replace_in_file("ZLMediaKit/CMakeLists.txt", "add_library(zlmediakit STATIC ${MediaKit_src_list})", ''' add_library(ZLMediaKit SHARED ${MediaKit_src_list}) ''')
        else:
        	tools.replace_in_file("ZLMediaKit/CMakeLists.txt", "add_library(zlmediakit STATIC ${MediaKit_src_list})", ''' add_library(ZLMediaKit STATIC ${MediaKit_src_list}) ''')
        	pass

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="ZLMediaKit")
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src="ZLMediaKit")
        self.copy("*ZLMediaKit.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="bin", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["ZLMediaKit"]

