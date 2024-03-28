import asyncio
import os
import carb
import logging
import omni.replicator.core as rep

logger = logging.getLogger(__name__)
logger.info("Logging with 'logging'")
carb.log_info("Logging with 'carb'")
rep.settings.carb_settings("/omni/replicator/RTSubframes", 1) #If randomizing materials leads to problems, try value 3

with rep.new_layer():
	def scatter_items(items):
		table = rep.get.prims(path_pattern='/World/SurgeryToolsArea')
		with items:
			rep.modify.pose(rotation=rep.distribution.uniform((0, 0, 0), (0, 360, 0)))
			rep.randomizer.scatter_2d(surface_prims=table, check_for_collisions=True)
		return items.node
	
	def randomize_camera():
		with camera:
			rep.modify.pose(
				position=rep.distribution.uniform((-10, 50, 50), (10, 120, 90)),
				look_at=(0, 0, 0))
		return camera
	
	def alternate_lights():
		with lights:
			rep.modify.attribute("intensity", rep.distribution.uniform(10000, 90000))
		return lights.node
	
	def randomize_screen(screen, texture_files):
		with screen:
			# Load a random .jpg file as texture
			rep.randomizer.texture(textures=texture_files)
		return screen.node

	rep.settings.set_render_pathtraced(samples_per_pixel=64)
	camera = rep.create.camera(position=(0, 24, 0))
	tools = rep.get.prims(semantics=[("class", "tweezers"), ("class", "scissors"), ("class", "scalpel"), ("class", "sponge")])
	backgrounditems = rep.get.prims(semantics=[("class", "background")])
	lights = rep.get.light(semantics=[("class", "spotlight")])
	screen = rep.get.prims(path_pattern='/World/SurgeryToolsArea')
	render_product = rep.create.render_product(camera, (320, 320))

	folder_path = 'C:/Users/eivho/source/repos/surgery-inventory-jetson/val2017/testing/'
	texture_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.jpg')]

	rep.randomizer.register(scatter_items)
	rep.randomizer.register(randomize_camera)
	rep.randomizer.register(alternate_lights)
	rep.randomizer.register(randomize_screen)
     
	with rep.trigger.on_frame(num_frames=10000, rt_subframes=20):
		rep.randomizer.scatter_items(tools)
		rep.randomizer.randomize_camera()
		rep.randomizer.alternate_lights()
		rep.randomizer.randomize_screen(screen, texture_files)

	writer = rep.WriterRegistry.get("BasicWriter")
	writer.initialize(
		output_dir="C:/Users/eivho/source/repos/surgery-inventory/Dataset/omniverse-replicator/out_texture2_320",
		rgb=True,
		bounding_box_2d_tight=True)

	writer.attach([render_product])
	asyncio.ensure_future(rep.orchestrator.step_async())