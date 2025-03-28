#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "core" for configuration "Release"
set_property(TARGET core APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(core PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lapkt/core/lib/libcore.so"
  IMPORTED_SONAME_RELEASE "libcore.so"
  )

list(APPEND _cmake_import_check_targets core )
list(APPEND _cmake_import_check_files_for_core "${_IMPORT_PREFIX}/lapkt/core/lib/libcore.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
