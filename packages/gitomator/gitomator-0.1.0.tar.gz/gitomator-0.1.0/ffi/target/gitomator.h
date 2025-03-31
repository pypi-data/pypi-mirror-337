#include <stdarg.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdlib.h>

/**
 * FFI-compatible Repository wrapper
 */
typedef struct GitRepository GitRepository;

/**
 * Error handling for FFI
 */
typedef struct GitResultCode {
  bool success;
  char *error_message;
} GitResultCode;

void gitomator_free_error(struct GitResultCode *result);

struct GitResultCode gitomator_init(const char *path, struct GitRepository **repo_out);

struct GitResultCode gitomator_open(const char *path, struct GitRepository **repo_out);

struct GitResultCode gitomator_clone(const char *url,
                                     const char *path,
                                     struct GitRepository **repo_out);

struct GitResultCode gitomator_add(struct GitRepository *repo,
                                   const char *const *paths,
                                   uintptr_t count);

struct GitResultCode gitomator_commit_all(struct GitRepository *repo, const char *message);

struct GitResultCode gitomator_create_branch(struct GitRepository *repo, const char *branch_name);

struct GitResultCode gitomator_list_branches(struct GitRepository *repo,
                                             char ***branches_out,
                                             uintptr_t *count_out);

void gitomator_free_branch_list(char **branches, uintptr_t count);

struct GitResultCode gitomator_get_hash(struct GitRepository *repo, bool short_, char **hash_out);

void gitomator_free_string(char *string);

void gitomator_free_repository(struct GitRepository *repo);
