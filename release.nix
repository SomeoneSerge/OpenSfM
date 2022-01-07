{ lib
, python
, buildPythonPackage
, toPythonModule
, symlinkJoin
, fetchFromGitHub
, cmake
, opencv
, opencv4
, ceres-solver
, suitesparse
, metis
, eigen
, pkg-config
, pybind11
, numpy
, pyyaml
, lapack
, gtest
, gflags
, gmock
, glog
, pytestCheckHook
, pytest
, networkx
, pillow
, exifread
, gpxpy
, pyproj
, dateutil
, joblib
, repoze_lru
, xmltodict
, cloudpickle
, scipy
}:

let
  pname = "OpenSfM";
  version = "0.5.1";
  src = fetchFromGitHub {
    owner = "mapillary";
    repo = "OpenSfM";
    rev = "v${version}";
    sha256 = "sha256-AU3n3AVgNWeRBFt5hnuzDVU4WEWhI9mmKUuARnFBY4c=";
    fetchSubmodules = true;
  };
  opensfm =
    buildPythonPackage {
      inherit pname version src;
      nativeBuildInputs = [ cmake pkg-config ];
      buildInputs = [
        opencv
        ceres-solver.dev
        suitesparse
        metis
        eigen
        lapack
        gflags
        gmock
        gtest
        glog
        python
      ];
      propagatedBuildInputs = [
        numpy
        scipy
        pyyaml
        opencv4
        networkx
        pillow
        exifread
        gpxpy
        pyproj
        dateutil
        joblib
        repoze_lru
        xmltodict
        cloudpickle
        pytest
      ];
      checkInputs = [ pytestCheckHook ];
      dontUseCmakeBuildDir = true;
      dontUseCmakeConfigure = true;
      cmakeFlags = [
        "-Bcmake_build"
        "-Sopensfm/src"
      ];
      patches = [ ./fix-cmake.patch ];
      postPatch = ''
        rm opensfm/src/cmake/FindEigen.cmake
        rm opensfm/src/cmake/FindCeres.cmake
        rm opensfm/src/cmake/FindGlog.cmake
        rm opensfm/src/cmake/FindGflags.cmake
        rm -rf opensfm/src/third_party/gtest
      '';
      meta = {
        maintainer = lib.maintainers.SomeoneSerge;
        license = lib.licenses.bsd2;
      };
    };
in
opensfm
