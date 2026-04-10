/**
 * ____        _           _                       
 * |  _ \ _   _| | ___ _ __| |_   _ _ __   __ _  ___ 
 * | |_) | | | | |/ _ \ '__| | | | | '_ \ / _` |/ _ \
 * |  _ <| |_| | |  __/ |  | | |_| | | | | (_| |  __/
 * |_| \_\\__,_|_|\___|_|  |_|\__,_|_| |_|\__,_|\___|
 * * Project: PARALLAX Effect
 * Author: Rulerlunae
 * Repository: https://github.com/Rulerlunae18/PARALAX
 * Description: Smooth, optimized parallax scrolling implementation.
 * * "Any sufficiently advanced bug is indistinguishable from a feature."
 */

default parallax_x = 0.0
default parallax_y = 0.0
default smooth_x = 0.0
default smooth_y = 0.0
default interpolated_x = 0.5
default interpolated_y = 0.5
default sensor_listener = None

init python in sensors:
    import store

    def initialize_sensor():
        try:
            renpy = getattr(store, "renpy", None)
            if not renpy or not renpy.android: return
        except Exception:
            return

        try:
            import jnius
            _Context = jnius.autoclass('android.content.Context')
            _Sensor = jnius.autoclass('android.hardware.Sensor')
            _SensorManager = jnius.autoclass('android.hardware.SensorManager')
            _PythonSDLActivity = jnius.autoclass('org.renpy.android.PythonSDLActivity')

            class AccelerometerSensorListener(jnius.PythonJavaClass):
                __javainterfaces__ = ['android/hardware/SensorEventListener']
                __javacontext__ = 'app'

                def __init__(self, onSensorChanged):
                    super(AccelerometerSensorListener, self).__init__()
                    self.onSensorChanged_cb = onSensorChanged

                @jnius.java_method('(Landroid/hardware/SensorEvent;)V')
                def onSensorChanged(self, event):
                    try:
                        self.onSensorChanged_cb(event.values[:3])
                    except: pass

                @jnius.java_method('(Landroid/hardware/Sensor;I)V')
                def onAccuracyChanged(self, sensor, accuracy):
                    pass

            def on_sensor_changed(values):
                try:
                    if not hasattr(store, 'smooth_x'): return

                    x = float(values[0])
                    y = float(values[1])
                    
                    raw_x = x / 10.0 + 0.5
                    raw_y = y / 10.0 + 0.5
                    
                    if raw_x < 0: raw_x = 0
                    if raw_x > 1: raw_x = 1
                    if raw_y < 0: raw_y = 0
                    if raw_y > 1: raw_y = 1

                    alpha = 0.2
                    store.smooth_x = (1 - alpha) * store.smooth_x + alpha * raw_x
                    store.smooth_y = (1 - alpha) * store.smooth_y + alpha * raw_y

                    store.parallax_x = store.smooth_y
                    store.parallax_y = 1.0 - store.smooth_x
                except: 
                    pass

            _mActivity = _PythonSDLActivity.mActivity
            _sensor_manager = jnius.cast(
                'android.hardware.SensorManager',
                _mActivity.getSystemService(_Context.SENSOR_SERVICE)
            )
            _sensor = _sensor_manager.getDefaultSensor(_Sensor.TYPE_ACCELEROMETER)

            store.sensor_listener = AccelerometerSensorListener(on_sensor_changed)
            
            _sensor_manager.registerListener(store.sensor_listener, _sensor, _SensorManager.SENSOR_DELAY_UI)
            
        except Exception:
            return

init python:
    def update_mouse_parallax():
        if renpy.android: return

        if renpy:
            pos = renpy.get_mouse_pos()
            sw = config.screen_width or 1920
            sh = config.screen_height or 1080
            renpy.store.parallax_x = pos[0] / float(sw)
            renpy.store.parallax_y = pos[1] / float(sh)

    if renpy.android:
        sensors.initialize_sensor()

    def interpolate_parallax():
        if not hasattr(store, 'interpolated_x'): return

        alpha = 0.1

        target_x = store.parallax_x
        target_y = store.parallax_y
        
        current_x = store.interpolated_x
        current_y = store.interpolated_y

        if abs(target_x - current_x) < 0.0005: 
            store.interpolated_x = target_x 
        else:
            store.interpolated_x = (1 - alpha) * current_x + alpha * target_x

        if abs(target_y - current_y) < 0.0005:
            store.interpolated_y = target_y
        else:
            store.interpolated_y = (1 - alpha) * current_y + alpha * target_y

    def reset_parallax():
        store.parallax_active = False
        store.parallax_x = 0.5
        store.parallax_y = 0.5
        store.interpolated_x = 0.5
        store.interpolated_y = 0.5
        store.smooth_x = 0.0
        store.smooth_y = 0.0

    class ParallaxLayer(renpy.Displayable):
        def __init__(self, image, depth=50, anchor=(0.5, 0.5), zoom=1.0, alpha=1.0, rotate=0):
            super(ParallaxLayer, self).__init__()
            
            self.child = Transform(image, zoom=zoom, alpha=alpha, rotate=rotate, subpixel=True)
            
            self.depth = depth
            self.anchor = anchor
            self.zoom = zoom
            self.alpha = alpha
            self.rotate = rotate

        def render(self, width, height, st, at): 
            cr = renpy.render(self.child, width, height, st, at)
            
            ix = getattr(store, "interpolated_x", 0.5)
            iy = getattr(store, "interpolated_y", 0.5)

            offset_x = (ix - 0.5) * self.depth
            offset_y = (iy - 0.5) * self.depth

            cw, ch = cr.get_size()
            
            x = (width * 0.5) - (cw * self.anchor[0]) + offset_x
            y = (height * 0.5) - (ch * self.anchor[1]) + offset_y

            rv = renpy.Render(width, height)
            rv.blit(cr, (x, y))

            if getattr(store, "parallax_active", False):
                renpy.redraw(self, 1.0 / 60.0) 

            return rv
