#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "planner" for configuration "Release"
set_property(TARGET planner APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(planner PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELEASE "core;wrapper"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lapkt/core/lib/planner.so"
  IMPORTED_SONAME_RELEASE "planner.so"
  )

list(APPEND _cmake_import_check_targets planner )
list(APPEND _cmake_import_check_files_for_planner "${_IMPORT_PREFIX}/lapkt/core/lib/planner.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
