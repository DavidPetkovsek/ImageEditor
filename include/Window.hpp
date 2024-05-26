#pragma once
#include <memory>
#include "imgui.h"
#include "imgui_impl_glfw.h"
#include "imgui_impl_opengl3.h"

struct Window{
    Window(int width, int height, const char *title, ImVec4 clear_color=ImVec4(0.45f, 0.55f, 0.60f, 1.00f));
    virtual void tick() = 0;
    virtual ~Window();

    virtual void run();
    virtual const char *glsl_version() const final;
protected:
    ImGuiIO *io;
    ImVec4 clear_color;
private:
    const char* _glsl_version;
    class Impl;
    std::shared_ptr<Impl> impl;
};