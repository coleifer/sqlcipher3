from conan import ConanFile

class OpensslRecipe(ConanFile):
    def requirements(self):
        self.requires('openssl/3.6.0')
